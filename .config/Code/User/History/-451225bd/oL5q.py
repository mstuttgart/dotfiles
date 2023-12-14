from odoo import  fields, models
from odoo.addons.br_account_einvoice_tecnospeed.models.const import TRIBUTACAO

STATE = {'edit': [('readonly', False)]}


class InvoiceElectronic(models.Model):
    _inherit = 'invoice.electronic'

    # webservice_nfse = fields.Selection(selection_add=[
    #     ('nfse_tecnospeed', 'Nota Fiscal Serviço (Tecnospeed)'),
    # ])

    tecnospeed_id_nota = fields.Char(string='ID Nota (tecnospeed)')

    # nfse_tecnospeed_natureza_operacao = fields.Selection(
    #     selection=NATUREZA_OPERACAO,
    #     string='Natureza da Operação (tecnospeed)',
    # )

    tecnospeed_regime_tributacao = fields.Selection(
        selection=TRIBUTACAO,
        string='Regime de Tributação (tecnospeed)',
        help='Código de identificação do regime especial de tributação',
    )

    tecnospeed_incentivador_cultural = fields.Boolean(
        string='Incentivador Cultural (tecnospeed)',
    )

    tecnospeed_incentivo_fiscal = fields.Boolean(
        string='Incentivador Cultural (Tecnospeed)',
    )

    # tecnospeed_nfse_pdf = fields.Binary(string='URL PDF')
    # tecnospeed_nfse_pdf_name = fields.Char(string='NFSe PDF Filename')
