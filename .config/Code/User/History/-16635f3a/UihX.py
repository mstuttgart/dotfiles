# © 2017 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    webservice_nfse = fields.Selection(selection_add=[
        ('nfse_ginfes', 'Nota Fiscal Serviço (ginfes)'),
    ])

    def _prepare_edoc_vals(self, invoice):
        """Cria um dict contendo os valores dos campos para serem
        utilizados na criação de registros da model 'invoice.electronic'

        Arguments:
            invoice {account.invoice} -- Fatura utilizada como base para inicializar os campos do invoice.electronic

        Returns:
            dict -- Dict para criação de 'invoice.electronic'
        """
        res = super(AccountInvoice, self)._prepare_edoc_vals(invoice=invoice)

        res['nfse_ginfes_tipo_rps'] = self.fiscal_position_id.nfse_ginfes_tipo_rps
        res['nfse_ginfes_natureza_operacao'] = self.fiscal_position_id.nfse_ginfes_natureza_operacao
        res['nfse_ginfes_regime_tributacao'] = self.company_id.nfse_ginfes_regime_tributacao
        res['nfse_ginfes_incentivador_cultural'] = self.company_id.nfse_ginfes_incentivador_cultural

        # municipio de Fortaleza
        if self.company_id.city_id == self.env.ref('br_base.city_3548807'):
            emissor = 'fortaleza'
        else:
            emissor = 'ginfes'


        nfse_ginfes_emissor

        return res