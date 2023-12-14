from odoo import api, fields, models
from odoo.addons.br_account_einvoice_tecnospeed.models.const import TRIBUTACAO, SEND_NFE_API

STATE = {'edit': [('readonly', False)]}


class InvoiceElectronic(models.Model):
    _inherit = 'invoice.electronic'

    tecnospeed_id_nota = fields.Char(string='ID Nota (tecnospeed)')

    nfe_engine = fields.Selection(
        selection=SEND_NFE_API,
        default='pytrustnfe',
        string='Engine para envio de NFe or NFSe'
    )

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

    @api.multi
    def _hook_validation(self):
        """Realiza validacao de campos criticos para emissao da NFSe e NFe.

        Returns:
            list: Lista de erros que detectados
        """

        errors = super(InvoiceElectronic, self)._hook_validation()

        if self.nfe_engine == 'tecnospeed':

            if self.company_id.tecnospeed_sandbox_active and not self.company_id.tecnospeed_certificado_id_sandbox:
                errors.append('Token para ambiente Sandbox obrigatório')

            if not self.company_id.tecnospeed_sandbox_active and not self.company_id.tecnospeed_certificado_id_producao:
                errors.append('Token para ambiente Produção/Homologação obrigatório')