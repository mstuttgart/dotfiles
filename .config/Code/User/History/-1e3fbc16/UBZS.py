
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

        self.env['pos.order.entry'].create({

        })
