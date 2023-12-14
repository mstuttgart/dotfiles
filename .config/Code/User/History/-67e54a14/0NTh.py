# © 2018 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    webservice_nfse = fields.Selection(selection_add=[
        ('nfse_goiania', 'Nota Fiscal Serviço (goiania)'),
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

        res['nfse_goiania_tipo_rps'] = self.fiscal_position_id.nfse_goiania_tipo_rps
        res['nfse_goiania_natureza_operacao'] = self.fiscal_position_id.nfse_goiania_natureza_operacao
        res['nfse_goiania_incentivador_cultural'] = self.company_id.nfse_goiania_incentivador_cultural

        return res
