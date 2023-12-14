{
    'name': 'Envio de NFSe Goiania',
    'description': """Efetua a integração com a prefeitura de Goiania""",
    'summary': """Efetua a integração com a prefeitura de Goiania""",
    'version': '12.0.1.0.0',
    'category': "Accounting & Finance",
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.multidados.tech',
    'contributors': [
        'Michell Stuttgart <michell.faria@multidados.tech>'
    ],
    'depends': [
        'br_nfse',
    ],
    'data': [
        'reports/danfse_goiania.xml',
        'views/account_fiscal_position.xml',
        'views/res_company.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
