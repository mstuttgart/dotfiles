
import getpass
import os
import pathlib
import subprocess

import click
import jinja2
import psycopg2


# Versao atual
VERSION = subprocess.run('git describe --abbrev=0', shell=True,
                         stdout=subprocess.PIPE).stdout.decode('utf8')[:-1]

# Capturamos o usuario linux
USER = getpass.getuser()

# Diretorio base do projeto
BASEDIR = pathlib.Path(__file__).parent.parent

# Monstamos os paths principais do projeto
TEMPLATE_PATH = os.path.join(BASEDIR, 'templates')
DATA_DIR = os.path.join(BASEDIR, 'multierp', 'database', 'odoo')
CONFIG_PATH = os.path.join(BASEDIR, 'multierp', 'config')
ADDONS_PATH = os.path.join(BASEDIR, 'multierp', 'src')
LIBS_PATH = os.path.join(BASEDIR, 'multierp', 'lib')

MODULE_TEMPLATE_PATH = os.path.join(BASEDIR, 'templates', 'module.template')

# Monstamos os paths principais do projeto
SERVER_PATH = '{}/core/odoo-bin'.format(ADDONS_PATH)


# Odoo addons
ADDONS = [
    'core/odoo/addons',
    'core/addons',
    'l10n_br',
    'multidadosti/channels-addons',
    'multidadosti/financial-addons',
    'multidadosti/lab88-addons',
    'multidadosti/jumaq-addons',
    'multidadosti/packages-addons',
    'multidadosti/private-addons',
    'multidadosti/public-addons',
    'multidadosti/report-addons',
    'multidadosti/web-addons',
    'muk',
    'formio',
    'oca/knowledge',
    'oca/multi-company',
    'oca/project',
    'oca/queue',
    'oca/report-engine',
    'oca/server-backend',
    'oca/server-tools',
    'oca/server-brand',
    'oca/server-ux',
    'oca/social',
    'oca/web',
    'others',
]


# Configuracoes de help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
def cli():
    pass


@cli.group(context_settings=CONTEXT_SETTINGS, chain=True)
def git():
    "Allow run git commands in all submodules."


@cli.group(context_settings=CONTEXT_SETTINGS, chain=True)
def release():
    """Usefull release commands."""


@cli.command()
def clean_pyc():
    """Clean all Python cache files.
    Exclude __pycache__ folder and *.pyc files."""
    click.secho(click.style('[INFO] Start cleanning', fg='green'))

    subprocess.call('find . -name \'*.pyc\' -exec rm -f {} +', shell=True)
    subprocess.call('find . -name \'*.pyo\' -exec rm -f {} +', shell=True)
    subprocess.call('find . -name \'*~\' -exec rm -f {} +', shell=True)
    subprocess.call(
        'find . -name \'__pycache__\' -exec rm -fr {} +', shell=True)
    click.secho(click.style('[INFO] Cleanning done', fg='green'))


@git.command()
@click.argument('command')
def foreach(command):
    """Execute a <str:command> in all submodules.
    \f
    Arguments:
        ctx {dict} -- Context of click commands.
        command {str} -- Command to run in submodules.
    """
    cmd = 'git submodule foreach "%s"' % command
    click.secho(click.style('[INFO] Running %s\n' % cmd, fg='green'))
    subprocess.call(cmd, shell=True)


@git.command()
@click.pass_context
def fetch(ctx):
    """Run 'git fetch' command in all submodules.
    \f
    Arguments:
        ctx {dict} -- Context of click commands.
    """
    ctx.invoke(foreach, command='git fetch --prune --all && echo')


@git.command()
@click.argument('branch')
@click.pass_context
def checkout(ctx, branch):
    """Run 'git checkout <str:branch>' command in all submodules.
    \f
    Arguments:
        ctx {dict} -- Context of click commands.
        branch {str} -- Branch to checkout.
    """
    ctx.invoke(foreach, command='git checkout %s | true && echo' % branch)


@git.command()
@click.argument('branch')
@click.pass_context
def reset(ctx, branch):
    """Run 'git reset --hard origin <str:branch>' command in all submodules.
    \f
    Arguments:
        ctx {dict} -- Context of click commands.
        branch {str} -- Branch to use in reset.
    """
    ctx.invoke(fetch)
    ctx.invoke(foreach, command='git stash && echo')
    ctx.invoke(checkout, branch=branch)
    ctx.invoke(foreach, command='git reset --hard origin/%s && echo' % branch)


@git.command()
@click.argument('branch')
@click.option('--remote', default='origin', help='Remote to pull changes.')
@click.pass_context
def pull(ctx, branch, remote):
    """Run 'git checkout <str:branch> and 'git pull <str:remote> <str:branch>'
    in all submodules.

    This <branch> must be a local branch.
    \f
    Arguments:
        ctx {dict} -- Context of click commands.
        branch {str} -- Branch to checkout and pull changes.
        remote {str} -- Remote to pull changes.
    """
    ctx.invoke(checkout, branch=branch)
    ctx.invoke(foreach, command='git pull --rebase %s %s && echo' %
               (remote, branch))


@git.command()
@click.pass_context
def diff(ctx):
    """Run 'git diff main develop' command in all submodules.

    \f
    Arguments:
        ctx {dict} -- Context of click commands.
    """
    ctx.invoke(foreach, command='git diff main develop')


@git.command()
@click.pass_context
def status(ctx):
    """Run 'git status' command in all submodules.

    \f
    Arguments:
        ctx {dict} -- Context of click commands.
    """
    ctx.invoke(foreach, command='git status && echo')


@git.command()
@click.pass_context
def updateall(ctx):
    """Update root folder of project and update develop and main branchs
    of all submodules.

    \f
    Arguments:
        ctx {dict} -- Context of click commands.
    """
    # Atualizamos branch principal do projeto
    subprocess.call('git fetch -p', shell=True)
    subprocess.call('git pull origin main', shell=True)

    # Usamos um stash para garantir que o comando nao
    # ira ser encerrado por causa de alterações não commitadas
    ctx.invoke(foreach, command='git stash && echo')

    # Atualiazamos os HEAD de cada submodulo
    ctx.invoke(fetch)

    # Sobrescrevemos o historico da branch develop local
    # com o conteudo da develop
    ctx.invoke(checkout, branch='develop')
    ctx.invoke(foreach, command='git reset --hard origin/develop && echo')

    # Atualizamos as branch main locais
    ctx.invoke(checkout, branch='main')
    ctx.invoke(foreach, command='git reset --hard origin/main && echo')


@git.command()
@click.option('-v', '--verbose', is_flag=True, default=False, help='Verbose output.')
@click.option('-r', '--remotes', is_flag=True, default=False, help='Show branchs for all remotes.')
@click.pass_context
def branch(ctx, verbose, remotes):
    """Run 'git branch' command in all submodules.
    \f
    Arguments:
        ctx {dict} -- Context of click commands.
        verbose {boolean} -- Flag to use verbose mode in output of command.
        remotes {boolean} -- Flag to show the others remotes in local repository.
    """
    command = 'git branch'
    command += ' --verbose' if verbose else ''
    command += ' --remotes' if remotes else ''
    command += ' && echo'

    ctx.invoke(foreach, command=command)


@git.command()
@click.argument('branch')
@click.pass_context
@click.confirmation_option(prompt='Are you sure you want to drop all local branchs?')
def clean(ctx, branch):
    """Delete all local branch with prefix <str:branch>-T[0-9].
    \f
    Arguments:
        ctx {dict} -- Context of click commands.
        branch {str} -- Base branch name to remove.
    """
    command = "git branch | grep \'%s-T[0-9]\' | xargs git branch -D || true && echo" % branch
    ctx.invoke(foreach, command=command)


@release.command()
@click.argument('tag')
@click.pass_context
@click.confirmation_option(prompt='Are you sure you want to create a new feature release?')
def feature(ctx, tag):
    """Use this command to create a new feature release with <str:tag>.

    This command run the follow actions:

    - fetch all submodules;\n
    - update (pull) 'develop' and 'main' branchs for all submodules;\n
    - rebase 'main 'branch with content of qa branch for all submodules;\n
    - commit and push 'main' branch to remote repository for all submodules;\n
    - create git tag from <tag> parameter and push it to project repository.\n

    \f
    Arguments:
        ctx {dict} -- Context of click commands.
        tag {str} -- Tag to new feature release. Use the format year.month.release.bugfix.
    """

    # O novo conteudo da branch 'main' vem dessa branch 'qa'.
    # Sendo assim, temos de garantir que a mesma esta atualizada
    # ctx.invoke(qa)

    ctx.invoke(checkout, branch='main')

    ctx.invoke(foreach, command='git reset --hard origin/develop && echo')
    ctx.invoke(foreach, command='git push -f origin main && echo')

    subprocess.call('git pull origin main', shell=True)

    # Monta os paths dos submodulos
    addons_path = [os.path.join('multierp', 'src', addon) for addon in ADDONS]

    for p in addons_path:

        # Simplificamos o path do core, porque o path do core
        # e diferente do path do submodulo. Isso evta com que
        # arquivos indesejados sejam adicionados
        if p in ('multierp/src/core/odoo/addons', 'multierp/src/core/addons'):
            p = 'multierp/src/core'

        subprocess.call('git add %s' % p, shell=True)

    # Adiciona alteracoes em libs
    subprocess.call('git add %s' % LIBS_PATH, shell=True)

    # Executamos git status em todos os submodulos para garantir
    # que esta tudo ok
    subprocess.call('manager git status', shell=True)

    if click.confirm('\nDo you want to continue and create release?', abort=True):

        click.secho(click.style('[INFO] Create update commit', fg='green'))

        subprocess.call('git commit -F task_list.txt', shell=True)
        subprocess.call('git push origin main', shell=True)

        click.secho(click.style('[INFO] Create version tag', fg='green'))

        subprocess.call('git tag -a %s -F task_list_tag.txt' % tag, shell=True)
        subprocess.call('git push --tags', shell=True)


@release.command()
@click.argument('tag')
@click.pass_context
@click.confirmation_option(prompt='Are you sure you want to create a new hotfix release?')
def hotfix(ctx, tag):
    """Use this command to create a new hotfix.

    This command run the follow actions:

    * fetch all submodules;\n
    * stash any uncommited changes for all submodules;\n
    * update (pull) main branch for all submodules;\n
    * commit and push main branch to remote repository for all submodules;\n
    * create git tag from <tag> parameter and push it to repository.
    \f
   Arguments:
        ctx {dict} -- Context of click commands.
        tag {str} -- Tag to new feature release. Use the format year.month.release.bugfix.
    """

    ctx.invoke(fetch)
    ctx.invoke(foreach, command='git stash && echo')

    # Atualiza develop com commits to hotfix
    ctx.invoke(checkout, branch='develop')
    ctx.invoke(foreach, command='git rebase origin/main')

    # Corrige historico da develop devido ao rebase com a main
    ctx.invoke(foreach, command='git pull --rebase origin develop')
    ctx.invoke(foreach, command='git push origin develop')

    # Atualizamos a main normalmente e seguimos o procedimento
    # de criacao do hotfix
    ctx.invoke(pull, branch='main')

    subprocess.call('git pull --rebase origin main', shell=True)

    # Monta os paths dos submodulos
    addons_path = [os.path.join('multierp', 'src', addon) for addon in ADDONS]

    for p in addons_path:

        # Simplificamos o path do core, porque o path do core
        # e diferente do path do submodulo. Isso evta com que
        # arquivos indesejados sejam adicionados
        if p in ('multierp/src/core/odoo/addons', 'multierp/src/core/addons'):
            p = 'multierp/src/core'

        subprocess.call('git add %s' % p, shell=True)

    # Adiciona alteracoes em libs
    subprocess.call('git add %s' % LIBS_PATH, shell=True)

    # Executamos git status em todos os submodulos para garantir
    # que esta tudo ok
    subprocess.call('manager git status', shell=True)

    if click.confirm('\nDo you want to continue and create hotfix?', abort=True):

        click.secho(click.style('[INFO] Create hotfix commit', fg='green'))

        subprocess.call('git commit -F task_list.txt', shell=True)
        subprocess.call('git push origin main', shell=True)

        click.secho(click.style('[INFO] Create version tag', fg='green'))

        subprocess.call('git tag -a %s -F task_list_tag.txt' % tag, shell=True)
        subprocess.call('git push --tags', shell=True)


@release.command()
@click.pass_context
def qa(ctx):
    """Use this command update qa branch. This branch will be used to test in QA enviromnent.

    This command run the follow actions:

    - fetch all submodules;\n
    - update (pull) 'develop' branchs for all submodules;\n
    - rebase 'qa' branch with content of develop branch for all submodules;\n
    - commit and push 'qa' branch to remote repository for all submodules;\n

    \f
    Arguments:
        ctx {dict} -- Context of click commands.
    """

    ctx.invoke(foreach, command='git stash && echo')
    ctx.invoke(fetch)
    ctx.invoke(pull, branch='develop')
    # ctx.invoke(checkout, branch='qa')

    # Conteudo da branch 'qa' e sobrescrito pela 'develop'
    ctx.invoke(foreach, command='git reset --hard origin/develop && echo')
    # ctx.invoke(foreach, command='git push -f origin qa && echo')

    click.secho(click.style('[INFO] qa branch updated', fg='green'))


# -----------------------
# Config Commands
# -----------------------


@cli.command()
def odooconf():
    """Render config file from template.
    """

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_PATH))

    # path de destino
    odoo_cfg_path = os.path.join(CONFIG_PATH, 'odoo.cfg')

    # Definimos o template a ser utilizado
    template = jinja_env.get_template('odoo.template.cfg')

    # Precisamos remover os espacos em branco de cada path
    addons_path = [os.path.join(ADDONS_PATH, addon) for addon in ADDONS]

    # Juntamos toda a lista em uma mesma string
    addons_path = ','.join(addons_path)

    # Renderiza template
    with open(odoo_cfg_path, 'w') as odoo_cfg_file:
        odoo_cfg_file.write(template.render(addons_path=addons_path,
                                            data_dir=DATA_DIR))

    click.secho(click.style('[INFO] Config file generated', fg='green'))


@cli.command()
@click.argument('database')
@click.option('-h', '--host', default='localhost', help='Database host address set in Odoo configuration file.')  # noqa
@click.option('-u', '--user', default='odoo', help='Database user set in Odoo configuration file.')  # noqa
@click.option('-p', '--password', default='odoo', help='Database password set in Odoo configuration file.')  # noqa
@click.pass_context
def todev(ctx, database, host, user, password):
    """Convert production database to development.

    This command change NFe and NFSe enviromnent to
    'homologation', disable email server and autobackup and
    update host in system parameters.
    \f
    Arguments:
        ctx {dict} -- Click context dict.
        database {str} -- Database to convert do development mode.
        host {str} -- Database host address (default='localhost').
        user {str} -- Database user (default='odoo').
        password {str} -- Database password (default='odoo').
    """

    click.secho(click.style('[INFO] Start process...', fg='green'))

    # Criamos a conexao com o banco
    con = psycopg2.connect(host=host,
                           database=database,
                           user=user,
                           password=password)

    cur = con.cursor()

    try:
        # Alteramos o ambiente da NFe de Venda
        cur.execute(
            "SELECT * from ir_model_fields where model = 'res.company' and name='tipo_ambiente'")

        if cur.fetchall():
            cur.execute("UPDATE res_company SET tipo_ambiente = '2'")

    except psycopg2.ProgrammingError as exc:
        print(exc)

    try:
        # Alteramos o ambiente da NFSe
        cur.execute(
            "SELECT * from ir_model_fields where model = 'res.company' and name='tipo_ambiente_nfse'")

        if cur.fetchall():
            cur.execute("UPDATE res_company SET tipo_ambiente_nfse = '2'")
    except psycopg2.ProgrammingError as exc:
        print(exc)

    try:
        # Alteramos as config. dos servidores de email de saida
        cur.execute("UPDATE ir_mail_server SET smtp_host = 'localhost'")
        cur.execute("UPDATE ir_mail_server SET name = 'localhost'")
        cur.execute("UPDATE ir_mail_server SET smtp_port = 1025")
        cur.execute("UPDATE ir_mail_server SET smtp_encryption = 'none'")
        cur.execute("UPDATE ir_mail_server SET smtp_user = ''")
        cur.execute("UPDATE ir_mail_server SET smtp_pass = ''")
    except psycopg2.ProgrammingError as exc:
        print(exc)

    try:

        # Desabilitamos os crons
        cur.execute("UPDATE ir_cron SET active = false")
    except psycopg2.ProgrammingError as exc:
        print(exc)

    try:
        # Reconfiguramos os paramentros de sistema abaixo
        cur.execute(
            "UPDATE ir_config_parameter SET value = 'http://localhost:8069/' WHERE key in ('web.base.url', 'report.url')")  # noqa
    except psycopg2.ProgrammingError as exc:
        print(exc)

    try:
        # Criamos uma hash para o novo password "admin"
        # Alteramos a senha do usuario admin
        cur.execute("UPDATE res_users SET password='admin' WHERE login='admin'")
    except psycopg2.ProgrammingError as exc:
        print(exc)

    # Persistimos as mudanças no banco de dados
    con.commit()

    click.secho(click.style('[INFO] Database %s updated' % database, fg='green'))  # noqa


@cli.command()
def clean_session():
    """Clean all DB session files"""
    click.secho(click.style('[INFO] Start cleanning session files', fg='green'))  # noqa
    subprocess.call('rm -rf multierp/database/odoo/sessions/*', shell=True)  # noqa
    click.secho(click.style('[INFO] Cleanning done', fg='green'))  # noqa


@cli.command()
@click.argument('name')
def scaffold(name):
    """Generates an Odoo module skeleton.

    \f
    Arguments:
        name {str} -- Name of the module to create.
    """

    cmd = [
        SERVER_PATH,
        'scaffold',
        '-t',
        MODULE_TEMPLATE_PATH,
        name,
    ]

    try:
        subprocess.call(cmd)
        click.secho(click.style(
            '[INFO] Module \'{}\' created!!'.format(name), fg='green'))

    except KeyboardInterrupt:
        click.secho(click.style('Done', fg='green'))


if __name__ == '__main__':
    cli()