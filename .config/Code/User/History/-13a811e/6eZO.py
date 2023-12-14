from odoo import models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _prepare_edoc_vals(self, invoice):
        """Cria um dict contendo os valores dos campos para serem
        utilizados na criação de registros da model 'invoice.electronic'

        Arguments:
            invoice {account.invoice} -- Fatura utilizada como base para inicializar os campos do invoice.electronic

        Returns:
            dict -- Dict para criação de 'invoice.electronic'
        """
        res = super(AccountInvoice, self)._prepare_edoc_vals(invoice=invoice)

        res['tecnospeed_regime_tributacao'] = self.company_id.tecnospeed_regime_tributacao
        res['tecnospeed_incentivador_cultural'] = self.company_id.tecnospeed_incentivador_cultural
        res['tecnospeed_incentivo_fiscal'] = self.company_id.tecnospeed_incentivo_fiscal

        if invoice.fiscal_document_id.code in ('55', '65'):

        return res
