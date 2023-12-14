from odoo import fields, models


class PosOrderEntryLine(models.Model):
    _name = 'pos.order.entry.line'
    _description = 'POS Order Entry Line'

    numero_venda = fields.Char(related='pos_order_entry_id.numero_venda')

    codigo_produto = fields.Char(string='Codigo Produto')
    nome_produto = fields.Char(string='Nome Produto')

    quantidade = fields.Char(string='Quatidade')
    preco = fields.Char(string='Preço')
    desconto = fields.Char(string='Desconto')

    total_liquido = fields.Char(string='Total Liquido')

    pos_order_entry_id = fields.Many2one('pos.order.entry',
                                         string='POS Order Entry')
