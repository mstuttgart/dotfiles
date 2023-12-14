{
    'name': 'Modulo base de NFe e NFS-e Tecnospeed',
    'summary': """Modulo base para integração com o PlugNotas (Tecnospeed)""",
    'description': 'Modulo base para integração com PlugNotas (Tecnospeed)',
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
        'views/invoice_electronic.xml',
        'views/res_company.xml',
        'views/res_config_settings.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
