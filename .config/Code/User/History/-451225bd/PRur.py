from odoo import fields, models
from odoo.addons.br_account_einvoice_tecnospeed.models.const import TRIBUTACAO

STATE = {'edit': [('readonly', False)]}


class InvoiceElectronic(models.Model):
    _inherit = 'invoice.electronic'

    tecnospeed_id_nota = fields.Char(string='ID Nota (tecnospeed)')

    tecnospeed_regime_tributacao = fields.Selection(
        selection=TRIBUTACAO,
        string='Regime de Tributação (tecnospeed)',
        help='Código de identificação do regime especial de tributação',
        state=STATE,
    )

    tecnospeed_incentivador_cultural = fields.Boolean(
        string='Incentivador Cultural (tecnospeed)',
        state=STATE,
    )

    tecnospeed_incentivo_fiscal = fields.Boolean(
        string='Incentivador Cultural (Tecnospeed)',
        state=STATE,
    )
