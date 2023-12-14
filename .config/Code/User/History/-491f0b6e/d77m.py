{
    'name': 'API PDV TDS Soluções',
    'version': '12.0.1.0.0',
    'author': 'MultidadosTI',
    'maintainer': 'MultidadosTI',
    'website': 'www.multidados.tech',
    'license': 'LGPL-3',
    'category': 'Extra',
    'summary': """
        Modulo com API REST para integração com PDV TDS Soluções""",
    'contributors': [
        'Michell Stuttgart <michellstut@gmail.com>',
    ],
    'depends': [
        'muk_rest',
        'br_pos_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_config.xml',
        'views/pos_session.xml',
        'views/pos_order.xml',
        'views/account_journal.xml',
        'views/pos_order_entry.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}