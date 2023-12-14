# © 2016 Danimar Ribeiro <danimaribeiro@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTFT

_logger = logging.getLogger(__name__)

STATE = {'edit': [('readonly', False)]}


class InvoiceElectronic(models.Model):
    _inherit = 'invoice.electronic'

    ambiente_nfse = fields.Selection(string='Ambiente NFSe',
                                     related='company_id.tipo_ambiente_nfse')

    webservice_nfse = fields.Selection(selection=[],
                                       readonly=True,
                                       states=STATE,
                                       string='Webservice NFSe')

    verify_code = fields.Char(string='Código Autorização',
                              size=20,
                              readonly=True,
                              states=STATE)

    numero_rps = fields.Integer(string='Número RPS',
                                readonly=True,
                                states=STATE)

    codigo_tributacao_municipio = fields.Char(string='Cód. Tribut. Munic.',
                                              help='Código de Tributação no Municipio')

    lote_code = fields.Char(string='Lote')

    state = fields.Selection(selection_add=[
        ('open', 'Aberto'),
    ])

    retencoes_federais = fields.Monetary(
        string='Retenções Federais',
        compute='_compute_total_retencoes',
    )

    @api.depends('valor_retencao_pis', 'valor_retencao_cofins',
                 'valor_retencao_irrf', 'valor_retencao_inss',
                 'valor_retencao_csll')
    def _compute_total_retencoes(self):
        """ Calcula o total de retenções """

        for item in self:

            total = item.valor_retencao_pis
            total += item.valor_retencao_cofins
            total += item.valor_retencao_irrf
            total += item.valor_retencao_inss
            total += item.valor_retencao_csll

            item.retencoes_federais = total

    def issqn_due_date(self):
        date_emition = self.data_emissao
        next_month = date_emition + relativedelta(months=1)
        due_date = date(next_month.year, next_month.month, 10)
        if due_date.weekday() >= 5:
            while due_date.weekday() != 0:
                due_date = due_date + timedelta(days=1)
        date_mask = "%d/%m/%Y"
        due_date = datetime.strftime(due_date, date_mask)
        return due_date

    @api.multi
    def action_print_einvoice_report(self):

        docs = self.search([('model', '=', '001'), ('id', 'in', self.ids)])

        if docs:

            if docs[0].invoice_id.company_id.report_nfse_id:

                # Pegamos a primeira porque todas as NFSe sao/devem ser da
                # mesma prefeitura
                report = docs[0].invoice_id.company_id.report_nfse_id

                action = report.report_action(docs)
                action['report_type'] = 'qweb-pdf'
                return action
            elif docs[0].:xml_to_send
                raise UserError(
                    'Não existe um template de relatorio para NFSe '
                    'selecionado para a empresa emissora desta Fatura. '
                    'Por favor, selecione um template no cadastro da '
                    'empresa')
        else:
            return super(InvoiceElectronic, self).action_print_einvoice_report()

    def get_nfse_observation_text(self):
        """Adicionamos texto para ser utilizado no campo de 'Outras Informacoes'
        do DANFE.

        Returns:
            str -- Texto do campo 'Outras Informacoes'
        """

        return ''

    def action_get_electronic_invoice_status(self):
        pass
