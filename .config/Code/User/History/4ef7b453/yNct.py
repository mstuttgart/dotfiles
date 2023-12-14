# © 2018 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Envio de NFSe Belo Horizonte',
    'description': """Efetua a integração com a prefeitura de Belo Horizonte""",
    'summary': """Efetua a integração com a prefeitura de Belo Horizonte""",
    'version': '12.0.1.0.0',
    'category': "Accounting & Finance",
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
        'Michell Stuttgart <mfaria@multidados.tech>'
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
