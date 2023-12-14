# © 2016 Danimar Ribeiro <danimaribeiro@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account E-Invoice',
    'summary': """Base Module for the Brazilian Invoice electronic_doc_id""",
    'description': """
    Base Module for the Brazilian Invoice electronic_doc_id
    """,
    'version': '12.0.1.0.0',
    'category': 'account',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'website': 'http://www.trustcode.com.br',
    'contributors': [
        'Danimar Ribeiro <danimaribeiro@gmail.com>',
        'Michell Stuttgart <michellstut@gmail.com>',
    ],
    'depends': [
        'document',
        'br_base',
        'br_mail',
        'br_account',
        'br_data_account',
    ],
    'data': [
        'data/ir_cron.xml',
        'data/res_groups.xml',
        'security/ir.model.access.csv',
        'security/invoice_electronic.xml',
        'views/invoice_electronic_item.xml',
        'views/invoice_electronic_event.xml',
        'views/invoice_electronic.xml',
        'views/account_invoice.xml',
        'views/account_fiscal_position.xml',
        'views/account_journal.xml',
        'views/access_emails.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
