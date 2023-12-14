from odoo import api, fields, models

from odoo.addons.rest_api_tdssolucoes_pdv.models.const import STATE


class PorOrderEntry(models.Model):
    _name = 'pos.order.entry'
    _description = 'Pos Order Entry'

    pos_config = fields.Char(string='POS Config')
    pos_session = fields.Char(string='POS Session')

    session_id = fields.Char(string='Session')
    fiscal_position_id = fields.Char(string='Fiscal Position')

    total_bruto = fields.Char(string='Total Bruto')
    total_desconto = fields.Char(string='Total Desconto')

    amount_total = fields.Char(string='Amount Total')
    amount_paid = fields.Char(string='Amount Paid')
    amount_tax = fields.Char(string='Amount Tax')
    amount_return = fields.Char(string='Amount Return')

    pricelist_id = fields.Char(string='Pricelist')
    location_id = fields.Char(string='Location')
    tipo_pag_pdv = fields.Char(string='Tipo Pag. PDV')

    partner_name = fields.Char('Partner Name')
    partner_cnpj_cpf = fields.Char(string='Partner CNPJ/CPF')

    numero_venda = fields.Char(string='Numero da Venda')

    pos_order_ids = fields.One2many('pos.order', string='Pos Orders')

    state = fields.Selection(STATE, string='State')
