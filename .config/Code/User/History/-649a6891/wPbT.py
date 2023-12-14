from odoo import fields, models
from odoo.addons.br_nfse_goiania.models.const import TIPORPS


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    nfse_goiania_tipo_rps = fields.Selection(
        selection=TIPORPS,
        default='1',
        string='Tipo de RPS (goiania)',
        help='Código de tipo de RPS (goiania)',
    )

    # nfse_goiania_natureza_operacao = fields.Selection(
    #     selection=NATUREZA_OPERACAO,
    #     default='1',
    #     string='Natureza da Operação (goiania)',
    #     help='Código de natureza da operação para webservice goiania',
    # )
