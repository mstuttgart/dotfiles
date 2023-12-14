from odoo import fields, models


from odoo.addons.br_nfse_ginfes.models.const import TIPORPS, NATUREZA_OPERACAO


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    nfse_ginfes_tipo_rps = fields.Selection(
        selection=TIPORPS,
        default='1',
        string='Tipo de RPS',
        help='Código de tipo de RPS (ginfes)',
    )

    nfse_ginfes_natureza_operacao = fields.Selection(
        selection=NATUREZA_OPERACAO,
        default='1',
        string='Natureza da Operação (ginfes)',
        help='Código de natureza da operação para webservice GINFES',
    )
