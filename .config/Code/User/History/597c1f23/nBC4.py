from odoo import api, fields, models
from odoo.addons.rest_api_tdssolucoes_pdv.models.const import FORMA_PAGAMENTO_SELECTION


class PosOrder(models.Model):

    _inherit = 'pos.order'

    order_from_pdv = fields.Boolean(
        string='Origem no PDV',
        default=False,
    )

    tipo_pag_pdv = fields.Selection(
        FORMA_PAGAMENTO_SELECTION,
        string='Meio de Pagamento',
    )

    total_bruto = fields.Float(
        string='Total Bruto',
        digits=0,
    )

    total_desconto = fields.Float(
        string='Total Desconto',
        digits=0,
    )

    config_id = fields.Many2one('pos.config',
                                related='session_id.config_id',
                                string='POS Config')


    @api.multi
    def cron_pos_base(self):
        """Metodo executado pelo cron para confirmar os
        pos.orders criados pela integração com PDV
        """
        super(PosOrder, self).cron_pos_base()

        # Buscando POS Order para Transformar em Sale Order
        pos_orders_ids = self.env['pos.order'].sudo().search([
            ('state', 'in', ['draft']),
            ('order_from_pdv', '=', True),
        ])

        for order in pos_orders_ids:

            journals = order.session_id.config_id.journal_ids.filtered(lambda r: r.tipo_pag_pdv and r.journal_user)  # noqa

            for journal in journals:

                if journal.tipo_pag_pdv == order.tipo_pag_pdv:

                    wiz = self.env['pos.make.payment'].create({
                        'journal_id': journals[0].id,
                        'session_id': order.session_id.id,
                        'amount': order.amount_total - order.amount_paid,
                    })

                    wiz.with_context(active_id=order.id).check()
