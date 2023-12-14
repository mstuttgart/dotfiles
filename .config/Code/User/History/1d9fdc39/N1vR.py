{
    'name': 'Envio de NFS-e Tecnospeed',
    'summary': """Permite o envio de NFS-e Tecnospeed através das faturas do Odoo""",
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
        'br_nfse',
    ],
    'data': [
        'views/account_fiscal_position.xml',
        'views/invoice_electronic.xml',
        # 'views/res_company.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
