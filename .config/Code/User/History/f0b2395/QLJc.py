from odoo import _, api, fields, models


class PosOrderEntryEvent(models.Model):
    _name = 'pos.order.entry.event'
    _description = 'Pos Order Entry Event'

    