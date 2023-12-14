from odoo import fields, models


class PosOrderEntryEvent(models.Model):
    _name = 'pos.order.entry.event'
    _description = 'Pos Order Entry Event'
    _order = 'id desc'

    name = fields.Char(string='Mensagem', readonly=True)

    pos_order_entry_id = fields.Many2one(
        'pos.order.entry',
        ondelete='cascade',
        string='POS Order Entry',
        readonly=True,
    )

    category = fields.Selection(
        selection=[
            ('info', 'Info'),
            ('warning', 'Aviso'),
            ('error', 'Erro'),
        ],
        string='Tipo',
    )

    create_date = fields.Datetime(
        string='Create Date',
        readonly=True,
    )
