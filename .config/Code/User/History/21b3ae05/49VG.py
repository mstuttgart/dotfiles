#!/usr/bin/env python
import sys
import time
import urllib

import click
import odoorpc
import yaml

# Configuracoes de help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

# ------------------------------

# MULTI SETTINGS

# Project ID (Multierp (Odoo))
MULTI_PROJECT_ID = 61

# Stage IDS
MULTI_CODE_REVIEW_STAGE_ID = 37
MULTI_TESTING_STAGE_ID = 242
MULTI_RELEASE_STAGE_ID = 266
MULTI_DONE_STAGE_ID = 53
MULTI_CANCELLED_STAGE_ID = 26

MULTI_HOTFIX_PROJECT_TAG = 73

MULTI_URL = 'multi.multidados.tech'

# ------------------------------

WAIT_TIME = 10  # seconds
TIMEOUT_SEC = WAIT_TIME * 3


def _check_connection(domain, database, login, password, dev=False):
    """Verifica conexão com o domain e tenta
    reconectar um dado número de vezes caso o
    servidor esteja offline.

    Args:
        domain (str): Dominio do servidor
        dev (bool, optional): Indica se o serviço esta no localhost.
        Usado para testes. Defaults to False.

    Returns:
        odoorpc: Objeto odoorpc criado para conexão
    """
    click.secho(click.style(f'[INFO] Iniciando conexão com o dominio {domain}'))  # noqa

    # Verificamos se o servidor esta online
    # Caso não esteja, esperamos WAIT_TIME segundos
    # e tentamos novamente até o liminte de WAIT_TIME tentativas

    odoo = None
    timeout_sec = TIMEOUT_SEC

    while not odoo and timeout_sec > 0:

        try:

            if not dev:
                # Use to production instance
                odoo = odoorpc.ODOO(domain, protocol='jsonrpc+ssl', port=443)  # noqa
            else:
                # Use to local development
                odoo = odoorpc.ODOO('localhost', port=8069)

        except urllib.error.HTTPError:
            time.sleep(WAIT_TIME)
            timeout_sec -= WAIT_TIME

    if not odoo:
        sys.exit('[ERROR] Falha na conexão o servidor. Abortando...')

    click.secho(click.style(f'[INFO] Iniciando login no banco {database}... '))  # noqa

    try:
        odoo.login(database, login=login, password=password)
    except odoorpc.error.Error:
        click.secho(click.style(f'[ERROR] Erro de conexão no banco {database}. Abortando... '))  # noqa
        sys.exit()

    # Set timeout
    odoo.config['timeout'] = 3600

    return odoo


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.argument('login')
@click.argument('password', required=False)
@click.option('--dev', is_flag=True, default=False, help='Use script in dev enviromnent.')
@click.option('--skip_confirmation', is_flag=True, default=False, help='Use to skip confirmation ask')
@click.password_option()
def move_tasks2test(login, password, dev, skip_confirmation):
    """Move all tasks in MultidadosTI Odoo Project to 'Testing' stage.

    Usefull in develop enviromnent.

    Project: multiERP ( Odoo )
    Estage: Testando

    \f
    Arguments:
        login {str} -- User login in Odoo.
        password {str} -- Password login in Odoo.
        dev {boolean} -- Flag to use OdooRPC in local development.
        skip_confirmation {boolean} -- Flag to skip confirmation process.
    """

    # Prepare the connection to the server
    odoo = _check_connection(
        domain=MULTI_URL,
        database='multi',
        login=login,
        password=password,
        dev=dev,
    )

    # Tasks in 'Code Review' stage from Multierp (Odoo) project
    task_ids = odoo.env['project.task'].search([
        ('project_id', '=', MULTI_PROJECT_ID),
        ('stage_id', '=', MULTI_CODE_REVIEW_STAGE_ID),
        ('kanban_state', '=', 'done'),
    ])

    # Read 'code' and 'name' fields of project.task model
    tasks = odoo.execute('project.task', 'read', task_ids, ['code', 'name'])

    click.secho(click.style(
        '\n[INFO] The follow tasks will be move to \'Testing\' stage.\n', fg='green'))

    for index, task in enumerate(tasks):
        print(f'[{index}] * {task["code"]} - {task["name"]}')

    if skip_confirmation or click.confirm('\nDo you want to continue?', abort=True):
        # Mudamos o estagio da tarefa para 'Testando'
        odoo.env['project.task'].write(
            task_ids, {'stage_id': MULTI_TESTING_STAGE_ID})

        click.secho(click.style(
            '\n[INFO] Tasks moved to \'Testing\' stage.\n', fg='green'))


@cli.command()
@click.argument('login')
@click.argument('password', required=False)
@click.option('--dev', is_flag=True, default=False, help='Use script in dev enviromnent.')
@click.option('--hotfix', is_flag=True, default=False, help='Mover apenas tarefas de hotfix')
@click.option('--skip_confirmation', is_flag=True, default=False, help='Use to skip confirmation ask')
@click.password_option()
def move_tasks2done(login, password, dev, hotfix, skip_confirmation):
    """Move all tasks in MultidadosTI Odoo Project to 'Done' stage.

    Usefull in develop enviromnent.

    Project: multiERP ( Odoo )
    Estage: Concluido

    \f
    Arguments:
        login {str} -- User login in Odoo.
        password {str} -- Password login in Odoo.
        dev {boolean} -- Flag to use OdooRPC in local development.
        skip_confirmation {boolean} -- Flaf to skip confirmation process.
    """

    # Prepare the connection to the server
    odoo = _check_connection(
        domain=MULTI_URL, database='multi', login=login, password=password, dev=dev)

    # normal tasks
    if not hotfix:

        # Tasks in 'Release' stage from Multierp (Odoo) project
        task_ids = odoo.env['project.task'].search([
            ('project_id', '=', MULTI_PROJECT_ID),
            ('stage_id', '=', MULTI_TESTING_STAGE_ID),
            ('kanban_state', '=', 'done'),
        ])

    else:
        # Hotfix tasks
        # Tasks in 'Code Review' stage and eith hotfix tag from Multierp (Odoo) project
        task_ids = odoo.env['project.task'].search([
            ('project_id', '=', MULTI_PROJECT_ID),
            ('stage_id', '=', MULTI_CODE_REVIEW_STAGE_ID),
            ('kanban_state', '=', 'done'),
            ('tag_ids', '=', MULTI_HOTFIX_PROJECT_TAG),
        ])

    # Tasks in 'Done' stage from Multierp (Odoo) project
    task_to_deactive_ids = odoo.env['project.task'].search([
        ('project_id', '=', MULTI_PROJECT_ID),
        ('stage_id', 'in', (MULTI_DONE_STAGE_ID, MULTI_CANCELLED_STAGE_ID)),
        ('active', '=', True),
    ])

    # Read 'code' and 'name' fields of project.task model
    tasks = odoo.execute('project.task', 'read', task_ids, ['code', 'name'])

    click.secho(click.style(
        '\n[INFO] As tarefas a abaixo serão movidas para o estagio \'Concluido\' \n', fg='green'))

    for index, task in enumerate(tasks):
        print(f'[{index}] * {task["code"]} - {task["name"]}')

    if skip_confirmation or click.confirm('\nDo you want to continue?', abort=True):

        # Arquiva antigas tarefas que ja estavam com concluidas
        # para que não se misturem com as novas tarefas
        # if not hotfix:
        #     odoo.env['project.task'].write(
        #         task_to_deactive_ids, {'active': False})

        # Mudamos o estagio das novas tarefas para 'Concluido'
        # odoo.env['project.task'].write(
        #     task_ids, {'stage_id': MULTI_DONE_STAGE_ID})
        
        tasks = odoo.execute('project.task', 'onchange_stage_id', task_ids)
        
        # for task_id in task_ids:
        #     task_obj = odoo.env['project.task'].browse(task_id)
        #     task_obj.onchange_stage_id()

        click.secho(click.style(
            '\n[INFO] Tasks moved to \'Done\' stage.\n', fg='green'))


@ cli.command()
@ click.argument('login')
@ click.argument('password')
@ click.option('--dev', is_flag=True, default=False, help='Use script in dev enviromnent.')
@ click.option('--hotfix', is_flag=True, default=False, help='Lista hotfix tasks.')
@ click.password_option()
def list_tasks2deploy(login, password, dev, hotfix):
    """List all tasks in MultidadosTI Odoo Project in 'Release' stage.

    Usefull in develop enviromnent.

    Project: multiERP ( Odoo )
    Estage: Concluido

    \f
    Arguments:
        login {str} -- User login in Odoo.
        password {str} -- Password login in Odoo.
        dev {boolean} -- Flag to use OdooRPC in local development.
        hotfix {boolean} -- Flag to list hotfix tasks.
    """

    # Prepare the connection to the server
    odoo = _check_connection(
        domain=MULTI_URL, database='multi', login=login, password=password, dev=dev)

    # normal tasks
    if not hotfix:

        # Tasks in 'Release' stage from Multierp (Odoo) project
        task_ids = odoo.env['project.task'].search([
            ('project_id', '=', MULTI_PROJECT_ID),
            ('stage_id', '=', MULTI_TESTING_STAGE_ID),
            ('kanban_state', '=', 'done'),
        ])

        msg = '\n[INFO] The follow tasks is in Release stage.\n'

    else:
        # Hotfix tasks
        # Tasks in 'Code Review' stage and eith hotfix tag from Multierp (Odoo) project
        task_ids = odoo.env['project.task'].search([
            ('project_id', '=', MULTI_PROJECT_ID),
            ('stage_id', '=', MULTI_CODE_REVIEW_STAGE_ID),
            ('kanban_state', '=', 'done'),
            ('tag_ids', '=', MULTI_HOTFIX_PROJECT_TAG),
        ])

        msg = '\n[INFO] The follow hotfix tasks in Code Review stage.\n'

    # Read 'code' and 'name' fields of project.task model
    tasks = odoo.execute('project.task', 'read', task_ids, ['code', 'name'])

    click.secho(click.style(msg, fg='green'))

    with open('tasks.txt', 'w') as task_file:
        for task in tasks:
            text = f'* {task["code"]} - {task["name"]}'
            click.secho(click.style(text, fg='green'))
            task_file.write(text)


@ cli.command()
@ click.argument('client')
@ click.argument('module_name')
def check_module_status(client, module_name):
    """Check module is installed or not.
    \f
    Arguments:
        client {str} -- Name of client to backup instances.
        module_name {str} -- Name of module to check install.
    """

    # Carregamos as configuracoes do arquivo 'multierp.yml'
    with open('./data/auth_keys.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Prepare the connection to the server
    odoo = _check_connection(domain=cfg[client]['host'],
                             database=cfg[client]['database'],
                             login='admin',
                             password=cfg[client]['adminpassword'])

    # Get ir cron
    modules = odoo.env['ir.module.module'].search([('name', '=', module_name), ('state', '=', 'installed')])  # noqa

    if modules:
        click.echo(click.style('[OK] Module %s IS installed in "%s" database' % (
            module_name, cfg[client]['database']), fg='red'))
    else:
        click.echo(click.style(
            '[OK] Module %s NOT IS installed' % module_name, fg='green'))


@ cli.command()
@ click.argument('client')
def make_backup(client):
    """Run backup of instances in *.yml configuration file.
    \f
    Arguments:
        client {str} -- Name of client to connect.
    """

    # Carregamos as configuracoes do arquivo 'multierp.yml'
    with open('./data/auth_keys.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    click.echo(click.style('Backup starting...', fg='green'))

    # Prepare the connection to the server
    odoo = _check_connection(domain=cfg[client]['host'],
                             database=cfg[client]['database'],
                             login='admin',
                             password=cfg[client]['adminpassword'])

    click.echo(click.style(f'Start backup of \"{cfg[client]["database"]}\" database', fg='green'))  # noqa

    # Get ir cron
    cron_ids = odoo.env['ir.cron'].search([('name', '=', 'Backup zip ftp')])  # noqa

    cron = odoo.env['ir.cron'].browse(cron_ids)

    # Execute backup
    cron.backup_btn()

    click.echo(click.style(
        f'Backup of \"{cfg[client]["database"]}\" database done!', fg='green'))


@ cli.command()
@ click.argument('client')
def check_queuejob_started(client):
    """Check queue job is started.
    \f
    Arguments:
        client {str} -- Name of client to connect.
    """

    # Carregamos as configuracoes do arquivo 'multierp.yml'
    with open('./data/auth_keys.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Prepare the connection to the server
    odoo = _check_connection(domain=cfg[client]['host'],
                             database=cfg[client]['database'],
                             login='admin',
                             password=cfg[client]['adminpassword'])

    # Get queue.job takss
    jobs_pending = odoo.env['queue.job'].search_count(
        [('state', '=',  'pending')])

    # if jobs_pending:
    click.echo(click.style(
        f'[OK] Queue Job pending count in \"{cfg[client]["database"]}\" database Is \"{jobs_pending}\"', fg='blue'))

    # Get queue.job
    jobs = odoo.env['queue.job'].search(
        [('state', 'in',  ('started', 'enqueued'))])

    if jobs:
        click.echo(click.style(
            f'[OK] Queue Job IS started in \"{cfg[client]["database"]}\" database', fg='green'))


@ cli.command()
@ click.argument('client')
def check_active_users_number(client):
    """Count the number of users.
    \f
    Arguments:
        client {str} -- Name of client to connect.
    """

    # Carregamos as configuracoes do arquivo 'multierp.yml'
    with open('./data/auth_keys.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Prepare the connection to the server
    odoo = _check_connection(domain=cfg[client]['host'],
                             database=cfg[client]['database'],
                             login='admin',
                             password=cfg[client]['adminpassword'])

    # Get queue.job
    count_users = odoo.env['res.users'].search_count([
        ('active', '=',  True),
        ('share', '=', 0),
    ])

    click.echo(click.style(
        f'[OK] Number of active users in \"{cfg[client]["database"]}\" database: {count_users}', fg='blue'))

    return count_users


@cli.command()
@click.argument('client')
def update_record(client):
    """Atualiza recordset do Odoo em lote
    \f
    Arguments:
        client {str} -- Name of client to connect.
    """

    # Carregamos as configuracoes do arquivo 'multierp.yml'
    with open('./data/auth_keys.yml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    # Prepare the connection to the server
    odoo = _check_connection(domain=cfg[client]['host'],
                             database=cfg[client]['database'],
                             login='admin',
                             password=cfg[client]['adminpassword'])

    modules = odoo.env['ir.module.module'].search([('name', '=', 'nome_modulo'), ('state', '=', 'installed')])  # noqa

    if modules:

        # pesquisa os registros
        objs_ids = odoo.env['model.model'].search([])

        # transforma em objeto
        objs = odoo.env['model.model'].browse(objs_ids)

        # realiza a alteracao
        objs.write({
            'campo': 'valor',
        })

        click.echo(click.style(
            f'[OK] Atualiza \"{cfg[client]["database"]}\"', fg='blue'))


if __name__ == '__main__':
    cli()
