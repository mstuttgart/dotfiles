from odoo.exceptions import UserError

from odoo import fields

from .test_common import TestCommon
from odoo.addons.account_financial_boleto.boleto.document import dict_boleto


class TestPaymentOrder(TestCommon):
    def setUp(self):
        super(TestPaymentOrder, self).setUp()

        # Excluir todos os regstros para não conflitar com
        # os testes em casos em que o banco de dados esta
        # populado
        self.main_company.partner_id.email_ids.unlink()

    def _return_payment_order(self, invoice):
        payment_order = self.env['payment.order'].create({
            'payment_mode_id': invoice.payment_mode_id.id,
        })

        invoice.action_br_account_invoice_open()

        payment_order.with_context({
            'moves': invoice.move_ids.ids,
        }).action_register_boleto()

        return payment_order

    def test_search_billings(self):
        payment_order = self.env['payment.order'].create({
            'name': 'Order Test',
        })

        with self.assertRaises(UserError):
            payment_order.search_billings()

        for payment_mode in self.payment_modes.values():
            payment_order.write({
                'payment_mode_id': payment_mode.id,
            })

            res = payment_order.search_billings()

            self.assertEqual(res['type'], 'ir.actions.act_window')
            self.assertEqual(res['res_model'], 'payment.order.billing')

    def test__compute_is_billet(self):
        payment_order = self.env['payment.order'].create({
            'name': 'Order Test',
        })

        for payment_mode in self.payment_modes.values():
            payment_order.write({
                'payment_mode_id': payment_mode.id,
            })
            payment_mode.operation_type = 'cnab'

            self.assertFalse(payment_order.is_billet)

            payment_mode.operation_type = 'cnab_billing_order'

            self.assertTrue(payment_order.is_billet)

    def test__compute_show_buttons(self):
        payment_order = self.env['payment.order'].create({
            'name': 'Order Test',
        })

        self.assertTrue(payment_order.show_search_billings)

        payment_order.with_context({
            'active_model': 'account_invoice'
        })._compute_show_buttons()

        self.assertTrue(payment_order.show_search_billings)

    def test_action_register_boleto(self):
        invoices = self._return_invoices()

        for invoice in invoices.values():
            self._update_customer_and_company()
            invoice.action_br_account_invoice_open()

            payment_order = self.env['payment.order'].create({
                'name': 'Order Test',
            })

            with self.assertRaises(UserError):
                payment_order.action_register_boleto()

            payment_order.write({
                'payment_mode_id': invoice.payment_mode_id.id,
            })

            payment_order.with_context({
                'moves': invoice.move_ids.ids,
            }).action_register_boleto()

            self.assertNotEqual(payment_order.billet_files, False)
            self.assertEqual(
                len(payment_order.line_ids), len(invoice.move_ids))

    def test_cancel_boleto(self):
        invoices = self._return_invoices()

        for invoice in invoices.values():
            self._update_customer_and_company()
            payment_order = self._return_payment_order(invoice)

            payment_order.cancel_boleto()

            self.assertEqual(payment_order.line_ids.ids, [])

            for move in invoice.move_ids:
                self.assertFalse(move.payment_line_id)
                self.assertFalse(move.payment_mode_id)
                self.assertFalse(move.nosso_numero)
                self.assertFalse(move.boleto_emitido)

    def test_confirm_cancel_boleto(self):
        payment_order = self.env['payment.order'].create({
            'name': 'Order Test',
        })
        res = payment_order.confirm_cancel_boleto()

        self.assertEqual(res['type'], 'ir.actions.act_window')
        self.assertEqual(res['res_model'], 'base.confirm.wizard')

    def test_validate_fields(self):
        payment_order_without_lines = self.env['payment.order'].create({
            'name': 'Order Test',
        })
        with self.assertRaises(UserError):
            payment_order_without_lines.validate_fields()

        invoices = self._return_invoices()
        self._update_customer_and_company()

        payment_order_with_partner_and_company_inconsistencies = (
            self._return_payment_order(next(iter(invoices.values()))))

        self.main_company.write({
            'legal_name': False,
            'cnpj_cpf': False,
            'district': False,
            'zip': False,
            'city_id': False,
            'state_id': False,
            'street': False,
            'number': False,
        })

        self.customer.write({
            'cnpj_cpf': False,
            'district': False,
            'zip': False,
            'city_id': False,
            'country_id': False,
            'state_id': False,
        })

        with self.assertRaises(UserError):
            (payment_order_with_partner_and_company_inconsistencies
                .validate_fields())

        self._update_customer_and_company()
        payment_order_with_partner_and_company_inconsistencies.validate_fields()

    def test_unlink(self):
        invoices = self._return_invoices()

        for invoice in invoices.values():
            self._update_customer_and_company()

            payment_order = self._return_payment_order(invoice)

            with self.assertRaises(UserError):
                payment_order.unlink()

            payment_order.billet_files = False

            moves = [line.move_id for line in payment_order.line_ids]
            payment_order.unlink()

            for move in moves:
                self.assertFalse(move.payment_line_id)
                self.assertFalse(move.payment_mode_id)
                self.assertFalse(move.nosso_numero)
                self.assertFalse(move.boleto_emitido)

    def test_send_billet_mail(self):
        invoices = self._return_invoices()
        self.main_company.partner_id.write({
            'email': 'company@email.com',
            'email_ids': [(0, 0, {
                'email': 'company@email.com',
                'mail_type': 'billet',
            })],
        })
        for invoice in invoices.values():
            self._update_customer_and_company()
            payment_order = self._return_payment_order(invoice)

            payment_order.send_billet_mail()

            mails_attachments = self.env['ir.attachment'].search([
                ('res_model', '=', 'payment.order.line')
            ])

            self.assertEqual(len(mails_attachments),
                             len(payment_order.line_ids))

            mails_attachments.unlink()

    def test_confirm_send_billet_mail(self):
        invoices = self._return_invoices()
        self.main_company.partner_id.write({
            'email': 'company@email.com',
            'email_ids': [(0, 0, {
                'email': 'company@email.com',
                'mail_type': 'billet',
            })],
        })
        invoice = [i for i in invoices.values()]
        self._update_customer_and_company()
        payment_order = self._return_payment_order(invoice[0])
        payment_order.line_ids.mail_state = 'sent'

        res = payment_order.confirm_send_billet_mail()

        self.assertEqual(res['type'], 'ir.actions.act_window')
        self.assertEqual(res['res_model'], 'base.confirm.wizard')

        payment_order.line_ids.mail_state = 'outgoing'

        res = payment_order.confirm_send_billet_mail()
        self.assertEqual(res, None)

    def test_generate_billet(self):
        invoices = self._return_invoices()

        for invoice in invoices.values():
            self._update_customer_and_company()

            cancel_invoice = invoice.copy()
            cancel_invoice.generate_parcel_entry(
                self.financial_operation, self.title_type)

            invoice.action_br_account_invoice_open()

            bill_search, payment_order = self._generate_order_billing(invoice)

            bill_search.transfer_billings()

            for line in payment_order.line_ids:
                res = line.generate_billet()

                move = line.move_id
                payment_mode = payment_order.payment_mode_id
                object_boleto = res[0]
                bank_class_payment_mode = (
                    dict_boleto[payment_mode.boleto_type][0])

                self.assertTrue(
                    isinstance(object_boleto, bank_class_payment_mode.boleto))
                self.assertEqual(move.payment_mode_id, payment_mode)
                self.assertEqual(line.payment_mode_id, payment_mode)
                self.assertNotEqual(line.billet_pdf, False)
                self.assertEqual(line.nosso_numero, move.nosso_numero)
                self.assertEqual(line.nosso_numero, object_boleto.nosso_numero)
                self.assertEqual(line.date_maturity,
                                 move.date_maturity_current)
                self.assertEqual(line.value, move.amount)
                self.assertEqual(line.value, float(object_boleto.valor))
                self.assertEqual(
                    line.date_maturity.strftime("%Y-%m-%d"), str(object_boleto.data_vencimento))

    def test_get_company_email(self):
        invoices = self._return_invoices()
        self._update_customer_and_company()

        self.main_company.partner_id.write({
            'email': 'company@email.com',
            'email_ids': [(0, 0, {
                'email': 'company@email.com',
                'mail_type': 'billet',
            })],
        })

        payment_order = (self._return_payment_order(
            next(iter(invoices.values()))))

        first_line = payment_order.line_ids[0]

        self.assertEqual(first_line.get_company_email(), 'company@email.com')

        self.main_company.partner_id.email_ids = [(5,)]

        self.main_company.partner_id.write({
            'email': 'c@email.com',
            'email_ids': [(0, 0, {
                'email': 'c@email.com',
                'mail_type': 'billet',
            })],
        })

        self.assertEqual(first_line.get_company_email(), 'c@email.com')

    def test_get_company_notify_email(self):
        invoices = self._return_invoices()
        self._update_customer_and_company()

        self.main_company.partner_id.write({
            'email': 'company@email.com',
            'email_ids': [(0, 0, {
                'email': 'company@email.com',
                'mail_type': 'notify-billet',
            })],
        })

        payment_order = (self._return_payment_order(
            next(iter(invoices.values()))))

        first_line = payment_order.line_ids[0]

        self.assertEqual(first_line.get_company_notify_email(),
                         'company@email.com')

        self.main_company.partner_id.email_ids = [(5,)]

        self.main_company.partner_id.write({
            'email': 'c@email.com',
            'email_ids': [(0, 0, {
                'email': 'c@email.com',
                'mail_type': 'notify-billet',
            })],
        })

        self.assertEqual(first_line.get_company_notify_email(), 'c@email.com')

    def test_get_locale_date(self):
        invoices = self._return_invoices()
        self._update_customer_and_company()

        payment_order = (self._return_payment_order(
            next(iter(invoices.values()))))
        first_line = payment_order.line_ids[0]

        first_line.date_maturity = fields.Date.to_date('2000-01-01')
        self.assertEqual(first_line.get_locale_date(), '01/01/2000')

        first_line.date_maturity = fields.Date.to_date('2012-04-11')
        self.assertEqual(first_line.get_locale_date(), '11/04/2012')

        first_line.date_maturity = fields.Date.to_date('1955-11-10')
        self.assertEqual(first_line.get_locale_date(), '10/11/1955')

        first_line.date_maturity = fields.Date.to_date('2012-03-25')
        self.assertEqual(first_line.get_locale_date(), '25/03/2012')

        first_line.date_maturity = fields.Date.to_date('2015-04-30')
        self.assertEqual(first_line.get_locale_date(), '30/04/2015')
