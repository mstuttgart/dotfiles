from odoo import api, fields, models


class PorOrderEntry(models.Model):
    _name = 'pos.order.entry'
    _description = 'Pos Order Entry'

    pos_config = fields.Char('POS Config')
    pos_session = fields.Char('POS Session')

    session_id = fields.Integer('Session')
    fiscal_position_id = fields.Integer('Fiscal Position')

    total_bruto = fields.Char('Total Bruto')