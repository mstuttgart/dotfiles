from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestPOSOrderEntry(TransactionCase):

    def setUp(self):
        super(TestPOSOrderEntry, self).setUp()

        self.main_company = self.env.ref('base.main_company')
        currency_real = self.env.ref('base.BRL')

        self.main_company.write({
            'name': 'MultidadosTI',
            'legal_name': 'MULTIDADOS INFORMATICA LTDA - EPP',
            'cnpj_cpf': '57.371.593/0001-10',
            'zip': '88037-240',
            'street': 'Vinicius de Moraes',
            'number': '42',
            'district': 'Centro',
            'country_id': self.env.ref('base.br').id,
            'state_id': self.env.ref('base.state_br_sp').id,
            'city_id': self.env.ref('br_base.city_3550308').id,
            'phone': '(11) 9999-8888',
        })

        vals = {}

        # Atribuir a moeda em empresas com moeda ja definida causa erro nos testes
        if not self.main_company.currency_id:
            vals['currency_id'] = currency_real.id

        vals['inscr_est'] = '323.672.319.201'

        self.main_company.write(vals)

        # self.pos_config = self.env.ref('point_of_sale.pos_config_main')
        self.company_id = self.ref('base.main_company')
        self.product = self.env.ref('product.product_product_4')
        self.partner_demo = self.env.ref('br_account.br_account_res_partner_1')

        test_sale_journal = journal_obj.create({'name': 'Sales Journal - Test',
                                                'code': 'TSJ',
                                                'type': 'sale',
                                                'company_id': main_company.id})

        all_pricelists = env['product.pricelist'].search([('id', '!=', excluded_pricelist.id)])
        all_pricelists.write(dict(currency_id=main_company.currency_id.id))

        main_pos_config.write({

                                                       },
                                                       )],

        fpos = self.env['account.fiscal.position'].create({
            'name': 'Venda',
            'position_type': 'product',
        })

        journal_vals = {
            'name': 'Cash Journal - Test',
                                                       'code': 'TSC',
                                                       'type': 'cash',
                                                       'company_id': self.main_company.id,
                                                       'journal_user': True,
                                                       }

        self.env['pos.config'].create({
            'default_fiscal_position_id': fpos,
            'stock_location_id': self.env.ref('stock.stock_location_stock'),
            'pricelist_id': self.pos_config.available_pricelist_ids[0],
                        'journal_id': test_sale_journal.id,
            'invoice_journal_id': test_sale_journal.id,
            'journal_ids': [(0, 0, {'name': 'Cash Journal - Test',
                                                       'code': 'TSC',
                                                       'type': 'cash',
                                                       'company_id': self.main_company.id,
                                                       'journal_user': True})],
        })

        # self.pos_config.default_fiscal_position_id = fpos
        # self.pos_config.stock_location_id = self.env.ref('stock.stock_location_stock')
        # self.pos_config.pricelist_id = self.pos_config.available_pricelist_ids[0]

        # create a new session
        self.pos_session = self.env['pos.session'].create({
            'user_id': 1,
            'config_id': self.pos_config.id
        })

        # I click on create a new session button
        # self.pos_config.open_session_cb()

        self.pos_session = self.env['pos.session'].search([('config_id', '=', self.pos_config.id)])

        lines = {
            'codigo_produto': self.product.default_code,
            'nome_produto': self.product.name,
            'quantidade': '1',
            'preco': '3,50',
            'desconto': '1,00',
            'total_liquido': '2.50',
        }

        vals = {
            'config_guid': self.pos_config.guid,
            'session_guid': self.pos_session.guid,
            'numero_venda': 'POS1234',
            'cliente_nome': self.partner_demo.name,
            'cliente_cnpj_cpf': self.partner_demo.cnpj_cpf,
            'cliente_endereco': self.partner_demo.street,
            'valor_venda': '12.00',
            'valor_desconto': '5,50',
            'valor_liquido': '6,50',
            'tipo_pag_pdv': '01',
            'pos_order_entry_line_ids': [(0, 0, lines)],
            'state': 'open',
        }

        self.pos_order_entry = self.env['pos.order.entry'].create(vals)

    def test_format_decimal_values(self):

        self.assertEqual(self.pos_order_entry._format_decimal_values('3.456,25'), 3456.25)
        self.assertEqual(self.pos_order_entry._format_decimal_values(3.45), 3.45)
        self.assertEqual(self.pos_order_entry._format_decimal_values('3,10'), 3.1)
        self.assertEqual(self.pos_order_entry._format_decimal_values('3.10'), 3.1)

    def test_unlink(self):

        with self.assertRaises(UserError):
            self.pos_order_entry.state = 'done'
            self.pos_order_entry.unlink()

        with self.assertRaises(UserError):
            self.pos_order_entry.state = 'open'
            self.pos_order_entry.unlink()

    def test_action_back_to_draft(self):

        with self.assertRaises(UserError):
            self.pos_order_entry.state = 'done'
            self.pos_order_entry.action_back_to_draft()

        self.pos_order_entry.state = 'error'
        self.pos_order_entry.action_back_to_draft()

        self.assertEqual(self.pos_order_entry.state, 'draft')

    def test_action_cancel_entry(self):

        with self.assertRaises(UserError):
            self.pos_order_entry.state = 'done'
            self.pos_order_entry.action_cancel_entry()

        self.pos_order_entry.state = 'error'
        self.pos_order_entry.action_cancel_entry()

        self.assertEqual(self.pos_order_entry.state, 'cancel')

    def test_action_confirm_entry(self):

        with self.assertRaises(UserError):
            self.pos_order_entry.state = 'done'
            self.pos_order_entry.action_confirm_entry()

        self.pos_order_entry.state = 'draft'
        self.pos_order_entry.action_confirm_entry()

        self.assertEqual(self.pos_order_entry.state, 'open')

    def test_action_convert_to_pos_order(self):

        self.assertFalse(self.pos_order_entry.pos_order_entry_event_ids)

        # realizamos a conversao do entry para pos.order
        self.pos_order_entry.action_convert_to_pos_order()

        self.assertTrue(self.pos_order_entry.pos_order_entry_event_ids)

        self.assertEqual(self.pos_order_entry.state, 'done')
        self.assertTrue(self.pos_order_entry.pos_order_id)

        pos_order = self.pos_order_entry.pos_order_id

        self.assertEqual(pos_order.fiscal_position_id, self.pos_config.default_fiscal_position_id)
        self.assertEqual(pos_order.location_id, self.pos_config.stock_location_id)
        self.assertEqual(pos_order.pricelist_id, self.pos_config.pricelist_id)

        self.assertEqual(pos_order.session_id.guid, self.pos_order_entry.session_guid)
        self.assertEqual(pos_order.config_id.guid, self.pos_order_entry.config_guid)

        self.assertEqual(pos_order.total_bruto, 12.0)
        self.assertEqual(pos_order.total_desconto, 5.50)
        self.assertEqual(pos_order.amount_total, 6.50)

        self.assertEqual(pos_order.partner_id, self.partner_demo)
        self.assertEqual(pos_order.tipo_pag_pdv, self.pos_order_entry.tipo_pag_pdv)
        self.assertEqual(pos_order.state, 'draft')

        self.assertTrue(pos_order.order_from_pdv)
        self.assertFalse(pos_order.amount_paid)
        self.assertFalse(pos_order.amount_tax)
        self.assertFalse(pos_order.amount_return)

        self.assertTrue(pos_order.lines)

        for entry_l, order_l in zip(self.pos_order_entry.pos_order_entry_line_ids, pos_order.lines):
            self.assertEqual(entry_l.codigo_produto, order_l.product_id.default_code)
            self.assertEqual(order_l.qty, 1)
            self.assertEqual(order_l.price_unit, 3.5)
            self.assertEqual(order_l.discount, 1.0)
            self.assertEqual(order_l.price_subtotal, 3.5)
            self.assertEqual(order_l.price_subtotal_incl, 2.5)
