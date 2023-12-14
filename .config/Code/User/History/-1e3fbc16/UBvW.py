
from odoo.tests.common import TransactionCase


class TestPOSOrderEntry(TransactionCase):

    def setUp(self):
        super(TestPOSOrderEntry, self).setUp()

        self.posorder = self.env['pos.order']
        self.possession = self.env['pos.session']
        self.company_id = self.ref('base.main_company')
        self.product4 = self.env.ref('product.product_product_4')
        self.partner4 = self.env.ref('base.res_partner_4')
        self.pos_config = self.env.ref('point_of_sale.pos_config_main')

        # create a new session
        self.pos_order_session0 = self.env['pos.session'].create({
            'user_id': 1,
            'config_id': self.pos_config.id
        })

        self.pricelist = self.env.ref('product.list0')
        self.pricelist.currency_id = self.env.user.company_id.currency_id

        for l in self.pos_config.available_pricelist_ids:
            l.currency_id = self.env.user.company_id.currency_id

        lines = []

        for item in json.loads(values['items']):

            lines.append((0, 0, {
                'codigo_produto': item.get('codigo_produto', ''),
                'nome_produto': item.get('nome_produto', ''),
                'quantidade': item.get('quantidade', ''),
                'preco': item.get('preco', ''),
                'desconto': item.get('desconto', ''),
                'total_liquido': item.get('total_liquido', ''),
            }))

        vals = {
            'config_guid': values.get('config_guid', ''),
            'session_guid': values.get('session_guid', ''),
            'numero_venda': values.get('numero_venda', ''),
            'cliente_nome': values.get('cliente', ''),
            'cliente_cnpj_cpf': values.get('cpf_cnpj', ''),
            'cliente_endereco': values.get('endereco', ''),
                'valor_venda': values.get('valor_venda', ''),
                'valor_desconto': values.get('valor_desconto', ''),
                'valor_liquido': values.get('valor_liquido', ''),
                'tipo_pag_pdv': values.get('tipo_pagamento', ''),
                'pos_order_entry_line_ids': lines,
                'state': 'open',
            }

            pos_order_entry = request.env['pos.order.entry'].create(vals)

        self.env['pos.order.entry'].create({

        })
