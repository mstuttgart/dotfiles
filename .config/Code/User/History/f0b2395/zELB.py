from odoo import _, api, fields, models


class PosOrderEntryEvent(models.Model):
    _name = 'pos.order.entry.event'
    _description = 'Pos Order Entry Event'
    _order = 'id desc'
    
    name = fields.Char(string='Mensagem', readonly=True, states=STATE)
    invoice_electronic_id = fields.Many2one(
        'invoice.electronic', string="Fatura Eletrônica",
        readonly=True, states=STATE,
        ondelete='cascade', index=True)
    state = fields.Selection(
        related='invoice_electronic_id.state', string="State")
    category = fields.Selection(string='Tipo', selection=[('info', 'Info'),
                                                          ('warning', 'Aviso'),
                                                          ('error', 'Erro')])