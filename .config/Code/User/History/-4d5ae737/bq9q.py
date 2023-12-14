{
    'name': 'Envio de NFS-e Tecnospeed',
    'summary': """Modulo base para integração daPermite o envio de NFS-e Tecnospeed através das faturas do Odoo""",
    'description': 'Envio de NFS-e - Tecnospeed',
    'version': '12.0.1.0.0',
    'category': 'account',
    'author': 'MultidadosTI',
    'license': 'AGPL-3',
    'website': 'http://www.multidados.tech',
    'contributors': [
        'Michell Stuttgart <michell.faria@multidadosti.com.br>',
    ],
    'depends': [
        'br_account_einvoice',
    ],
    'data': [
        'views/res_company.xml',
        'views/res_config_settings.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
