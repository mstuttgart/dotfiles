# © 2009 Renato Lima - Akretion
# © 2016 Danimar Ribeiro, Trustcode
# © 2017 Michell Stuttgart, MultidadosTI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import copy
import locale

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = ['account.invoice', 'record.block.mixin']

    STATES = {
        'draft': [('readonly', False)],
    }

    def _get_default_stage_id(self):
        """ Gives minimum sequence stage
        Returns:
            Int -> retorna o menor ID possível para o estagio.
        """
        return self.env['account.invoice.stage'].search([], order="sequence, id desc", limit=1).id  # noqa

    payment_term_id = fields.Many2one(
        ondelete='restrict',
    )

    account_group_id = fields.Many2one(
        'account.group',
        string='Account Group',
        index=True,
        domain=[('account_ids', '=', False)],
        ondelete='restrict',
        track_visibility='onchange',
        help="Use the Financial Group for Reports, Dashboards and Statistics."
    )

    account_analytic_ids = fields.Many2many(
        comodel_name='account.analytic.account',
        compute='_compute_analytic_accounts',
        search='_search_analytic_accounts',
        string='Analytic Account',
        readonly=True,
        store=True
    )

    total_tax = fields.Float(string='Impostos ( + )',
                             readonly=True,
                             compute='_compute_amount',
                             digits=dp.get_precision('Account'),
                             store=True)

    parcel_ids = fields.One2many(comodel_name='br_account.invoice.parcel',
                                 inverse_name='invoice_id',
                                 readonly=True,
                                 states=STATES,
                                 string='Parcelas')

    parcels_date_maturity = fields.Text(string='Datas de Vencimento',
                                        compute="_compute_parcels_date_maturity")

    move_ids = fields.One2many('account.move',
                               inverse_name='invoice_id',
                               readonly=True,
                               string='Account Move')

    issuer = fields.Selection([('0', 'Terceiros'),
                               ('1', 'Emissão própria')],
                              string='Emitente',
                              default='0',
                              readonly=True,
                              states=STATES)

    vendor_number = fields.Char(string='Número NF Entrada',
                                size=18,
                                readonly=True,
                                states=STATES,
                                help='Número da Nota Fiscal do Fornecedor')

    vendor_serie = fields.Char(string='Série NF Entrada',
                               size=12,
                               help="Série do número da Nota Fiscal do "
                                    "Fornecedor")

    document_serie_id = fields.Many2one('br_account.document.serie',
                                        string='Série',
                                        readonly=True,
                                        default=False,
                                        states=STATES)

    fiscal_document_id = fields.Many2one('br_account.fiscal.document',
                                         string='Documento',
                                         readonly=True,
                                         states=STATES)

    journal_type = fields.Selection(string='Journal Type',
                                    related='journal_id.type')

    invoice_model = fields.Char(string='Modelo de Fatura',
                                related='fiscal_document_id.code',
                                readonly=True)

    pre_invoice_date = fields.Date(string='Data da Pré-Fatura',
                                   required=True,
                                   copy=False,
                                   default=fields.Date.today)

    cancel_invoice_date = fields.Date(string='Data da Cancelamento',
                                      readonly=True,
                                      copy=False)

    date_invoice = fields.Date(copy=False)

    internal_number = fields.Integer(string='Invoice Number',
                                     readonly=True,
                                     copy=False,
                                     group_operator=None,
                                     states={'draft': [('readonly', False)]},
                                     help="""Unique number of the invoice,
                                     computed automatically when the invoice
                                     is created.""")

    number_backup = fields.Char(copy=False,
                                string='Número do Pedido')

    is_electronic = fields.Boolean(related='fiscal_document_id.electronic',
                                   type='boolean',
                                   store=True,
                                   string='Eletrônico',
                                   readonly=True,
                                   oldname='is_eletronic')

    fiscal_document_related_ids = fields.One2many('br_account.document.related',
                                                  'invoice_id',
                                                  string='Documento Fiscal Relacionado',
                                                  readonly=True,
                                                  states=STATES)

    fiscal_observation_ids = fields.Many2many('br_account.fiscal.observation',
                                              string='Observações Fiscais',
                                              readonly=True,
                                              states=STATES)

    fiscal_comment = fields.Text('Observação Fiscal',
                                 readonly=True,
                                 states=STATES)

    total_bruto = fields.Float(string='Total Bruto ( = )',
                               store=True,
                               digits=dp.get_precision('Account'),
                               compute='_compute_amount')

    total_desconto = fields.Float(string='Desconto Financeiro ( - )',
                                  store=True,
                                  readonly=True,
                                  digits=dp.get_precision('Account'),
                                  compute='_compute_amount')

    icms_base = fields.Float(string='Base ICMS',
                             store=True,
                             compute='_compute_amount',
                             digits=dp.get_precision('Account'))

    icms_value = fields.Float(string='Valor ICMS',
                              digits=dp.get_precision('Account'),
                              compute='_compute_amount',
                              store=True)

    icms_credit_value = fields.Float(string='Valor ICMS Crédito',
                                     digits=dp.get_precision('Account'),
                                     compute='_compute_amount',
                                     store=True)

    icms_st_base = fields.Float(string='Base ICMS ST',
                                store=True,
                                compute='_compute_amount',
                                digits=dp.get_precision('Account'))

    icms_st_value = fields.Float(string='Valor ICMS ST',
                                 store=True,
                                 compute='_compute_amount',
                                 digits=dp.get_precision('Account'))

    valor_icms_fcp_uf_dest = fields.Float(string='Total ICMS FCP',
                                          store=True,
                                          compute='_compute_amount',
                                          help='Total total do ICMS relativo'
                                               ' Fundo de Combate à Pobreza '
                                               '(FCP) da UF de destino')

    valor_icms_uf_dest = fields.Float(string='ICMS Destino',
                                      store=True,
                                      compute='_compute_amount',
                                      help='Valor total do ICMS Interestadual'
                                           ' para a UF de destino')

    valor_icms_uf_remet = fields.Float(string='ICMS Remetente',
                                       store=True,
                                       compute='_compute_amount',
                                       help='Valor total do ICMS Interestadual'
                                            ' para a UF do Remetente')

    issqn_base = fields.Float(string='Base ISSQN',
                              store=True,
                              digits=dp.get_precision('Account'),
                              compute='_compute_amount')

    issqn_value = fields.Float(string='Valor ISSQN',
                               store=True,
                               digits=dp.get_precision('Account'),
                               compute='_compute_amount')

    issqn_retention = fields.Float(string='ISSQN Retido',
                                   store=True,
                                   digits=dp.get_precision('Account'),
                                   compute='_compute_amount')

    ipi_base = fields.Float(string='Base IPI',
                            store=True,
                            digits=dp.get_precision('Account'),
                            compute='_compute_amount')

    ipi_base_other = fields.Float(string="Base IPI Outras",
                                  store=True,
                                  digits=dp.get_precision('Account'),
                                  compute='_compute_amount')

    ipi_value = fields.Float(string='Valor IPI',
                             store=True,
                             digits=dp.get_precision('Account'),
                             compute='_compute_amount')

    pis_base = fields.Float(string='Base PIS',
                            store=True,
                            digits=dp.get_precision('Account'),
                            compute='_compute_amount')

    pis_value = fields.Float(string='Valor PIS',
                             store=True,
                             digits=dp.get_precision('Account'),
                             compute='_compute_amount')

    pis_retention = fields.Float(string='PIS Retido',
                                 store=True,
                                 digits=dp.get_precision('Account'),
                                 compute='_compute_amount')

    cofins_base = fields.Float(string='Base COFINS',
                               store=True,
                               digits=dp.get_precision('Account'),
                               compute='_compute_amount')

    cofins_value = fields.Float(string='Valor COFINS',
                                store=True,
                                digits=dp.get_precision('Account'),
                                compute='_compute_amount',
                                readonly=True)

    cofins_retention = fields.Float(string='COFINS Retido',
                                    store=True,
                                    digits=dp.get_precision('Account'),
                                    compute='_compute_amount',
                                    readonly=True)

    ii_value = fields.Float(string='Valor II',
                            store=True,
                            digits=dp.get_precision('Account'),
                            compute='_compute_amount')

    csll_base = fields.Float(string='Base CSLL',
                             store=True,
                             digits=dp.get_precision('Account'),
                             compute='_compute_amount')

    csll_value = fields.Float(string='Valor CSLL',
                              store=True,
                              digits=dp.get_precision('Account'),
                              compute='_compute_amount')

    csll_retention = fields.Float(string='CSLL Retido',
                                  store=True,
                                  digits=dp.get_precision('Account'),
                                  compute='_compute_amount')

    irrf_base = fields.Float(string='Base IRRF',
                             store=True,
                             digits=dp.get_precision('Account'),
                             compute='_compute_amount')

    irrf_value = fields.Float(string='Valor IRRF',
                              store=True,
                              digits=dp.get_precision('Account'),
                              compute='_compute_amount')

    irrf_retention = fields.Float(string='IRRF Retido',
                                  store=True,
                                  digits=dp.get_precision('Account'),
                                  compute='_compute_amount')

    inss_base = fields.Float(string='Base INSS',
                             store=True,
                             digits=dp.get_precision('Account'),
                             compute='_compute_amount')

    inss_value = fields.Float(string='Valor INSS',
                              store=True,
                              digits=dp.get_precision('Account'),
                              compute='_compute_amount')

    inss_food_voucher = fields.Float(string='Vale-Alimentação',
                                     digits=dp.get_precision('Account'),
                                     store=True,
                                     compute='_compute_amount')

    inss_transportation_voucher = fields.Float(string='Vale-Tranporte',
                                               digits=dp.get_precision('Account'),  # noqa
                                               store=True,
                                               compute='_compute_amount')

    inss_tools_supplies = fields.Float(string='Equipamentos/Materiais',
                                       digits=dp.get_precision('Account'),
                                       store=True,
                                       compute='_compute_amount')

    inss_deduction_total = fields.Float(string='Total Deduções do INSS',
                                        digits=dp.get_precision('Account'),
                                        store=True,
                                        compute='_compute_amount')

    inss_retention = fields.Float(string='INSS Retido',
                                  store=True,
                                  digits=dp.get_precision('Account'),
                                  compute='_compute_amount')

    total_tributos_federais = fields.Float(string='Total de Tributos Federais',
                                           store=True,
                                           digits=dp.get_precision('Account'),
                                           compute='_compute_amount')

    total_tributos_estaduais = fields.Float(string='Total de Tributos Estaduais',
                                            store=True,
                                            digits=dp.get_precision('Account'),
                                            compute='_compute_amount')

    total_tributos_municipais = fields.Float(string='Total de Tributos Municipais',
                                             store=True,
                                             digits=dp.get_precision(
                                                 'Account'),
                                             compute='_compute_amount')

    total_tributos_estimados = fields.Float(string='Total de Tributos',
                                            store=True,
                                            digits=dp.get_precision('Account'),
                                            compute='_compute_amount')

    chave_de_acesso = fields.Char(string='Chave de Acesso', size=44)

    block_draft_invoice = fields.Boolean(default=False)

    service_locale = fields.Selection(string='Serviço Prestado',
                                      selection=[
                                          ('1', 'No Município'),
                                          ('2', 'Fora do Município'),
                                      ],
                                      readonly=True,
                                      states=STATES,
                                      default='1')

    public_location = fields.Boolean(string='Via Pública',
                                     readonly=True,
                                     states=STATES)

    position_type = fields.Selection(string='Fiscal Position Type',
                                     related='fiscal_position_id.position_type')

    financial_price_total = fields.Monetary(
        string='Financial Total',
        store=True,
        default=0.00,
        readonly=True,
        compute='_compute_amount',
        help="""The Financial Total shows the gross amount added to the taxes marked to be added to the total amount of the installments"""
    )

    bank_account_for_expected = fields.Many2one(
        'account.journal',
        domain=lambda self: ['&', ('type', 'in', ['bank', 'cash']), ('company_id', '=', self.env.user.company_id.id)]  # noqa
    )

    partner_bank_id = fields.Many2one(string='Partner Bank Account')

    service_locale_address_id = fields.Many2one('res.partner',
                                                string='Endereço de Prestação de Serviço')

    anticipated_value = fields.Monetary(
        string='Anticipated Value',
        store=True,
        default=0.00,
        compute='_compute_anticipated_value')

    anticipated_residual_value = fields.Monetary(
        string='Anticipated Residual',
        store=True,
        default=0.00,
        compute='_compute_anticipated_value')

    anticipated_residual_payment = fields.Monetary(
        string='Payment Anticipated Residual',
        store=True,
        default=0.00,
        compute='_compute_anticipated_value')

    custom_stage_id = fields.Many2one(
        'account.invoice.stage',
        string="Stage",
        ondelete='restrict',
        track_visibility='onchange',
        index=True,
        default=_get_default_stage_id,
        copy=False
    )

    custom_stage_color = fields.Many2many(
        'account.invoice.stage',
        compute='_compute_stage_color',
        readonly=True
    )

    state = fields.Selection(
        selection_add=[
            ('blocked', 'Blocked'),
            ('processing', 'Processing'),
        ])

    client_order_ref = fields.Char(
        string='Customer Reference',
        size=15,
        copy=False,
        readonly=True,
        states=STATES
    )

    partner_legal_name = fields.Char(
        related='partner_id.legal_name',
    )

    partner_cnpj_cpf = fields.Char(
        related='partner_id.cnpj_cpf',
    )

    discount_type = fields.Selection(
        [('percent', 'Percentage'),
         ('amount', 'Amount')],
        string='Discount type',
        readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        default='percent'
    )

    discount_rate = fields.Float(
        'Discount Rate',
        digits=dp.get_precision('Account'),
        readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}
    )

    origin = fields.Char(copy=False)

    reload_taxes = fields.Boolean(
        string='Recarregar Impostos',
        default=False,
    )

    financial_identifier = fields.Char(
        string='Financial Identifier',
    )

    @api.multi
    @api.depends("invoice_line_ids.account_analytic_id")
    def _compute_analytic_accounts(self):
        for invoice in self:
            invoice.account_analytic_ids = invoice.mapped('invoice_line_ids.account_analytic_id.id')  # noqa

    @api.multi
    def _search_analytic_accounts(self, operator, value):
        return [('invoice_line_ids.account_analytic_id', operator, value)]

    @api.multi
    @api.depends('parcel_ids', 'parcel_ids.parceling_value', 'parcel_ids.anticipated_payment', 'parcel_ids.move_state')
    def _compute_anticipated_value(self):

        if self.check_access_rule_bool('write'):
            invoices = self
        else:
            invoices = self.sudo()

        for invoice in invoices:
            anticipated_value = 0
            anticipated_residual_value = 0
            anticipated_residual_payment = 0

            if invoice.parcel_ids:

                for parcel in invoice.parcel_ids.filtered(lambda r: r.anticipated_payment):
                    # Valor Total da Antecipação
                    anticipated_value += parcel.parceling_value

                    # Valor a Gerar Título (Pendente)
                    if parcel.move_state == 'none':
                        anticipated_residual_value += parcel.parceling_value

                    # Valor a Receber (Pendente)
                    if parcel.move_ids:
                        anticipated_residual_payment += sum(m.amount_residual for m in parcel.move_ids)  # noqa
                    else:
                        anticipated_residual_payment += parcel.parceling_value

            invoice.anticipated_value = anticipated_value
            invoice.anticipated_residual_value = anticipated_residual_value
            invoice.anticipated_residual_payment = anticipated_residual_payment

    @api.one
    @api.depends('invoice_line_ids.price_subtotal',
                 'invoice_line_ids.price_total',
                 'invoice_line_ids.financial_price_total',
                 'tax_line_ids.amount',
                 'currency_id', 'company_id')
    def _compute_amount(self):
        super(AccountInvoice, self)._compute_amount()

        values = {
            'total_tax': 0,
            'icms_base': 0,
            'icms_value': 0,
            'icms_credit_value': 0,
            'icms_st_base': 0,
            'icms_st_value': 0,
            'valor_icms_uf_remet': 0,
            'valor_icms_uf_dest': 0,
            'valor_icms_fcp_uf_dest': 0,
            'issqn_base': 0,
            'issqn_value': 0,
            'ipi_base': 0,
            'ipi_value': 0,
            'pis_base': 0,
            'pis_value': 0,
            'cofins_base': 0,
            'cofins_value': 0,
            'ii_value': 0,
            'csll_base': 0,
            'csll_value': 0,
            'irrf_base': 0,
            'irrf_value': 0,
            'inss_base': 0,
            'inss_value': 0,
            'inss_food_voucher': 0,
            'inss_transportation_voucher': 0,
            'inss_tools_supplies': 0,
            'pis_retention': 0,
            'cofins_retention': 0,
            'csll_retention': 0,
            'irrf_retention': 0,
            'inss_retention': 0,
            'total_bruto': 0,
            'total_desconto': 0,
            'financial_price_total': 0,
            'total_tributos_federais': 0,
            'total_tributos_estaduais': 0,
            'total_tributos_municipais': 0,
            'total_tributos_estimados': 0,
        }

        for line in self.invoice_line_ids:

            values['total_tax'] += line.price_tax

            values['icms_base'] += line.icms_base_calculo
            values['icms_value'] += line.icms_valor
            values['icms_st_base'] += line.icms_st_base_calculo
            values['icms_st_value'] += line.icms_st_valor

            values['icms_credit_value'] += line.icms_valor_credito

            values['valor_icms_uf_remet'] += line.icms_uf_remet
            values['valor_icms_uf_dest'] += line.icms_uf_dest
            values['valor_icms_fcp_uf_dest'] += line.icms_fcp_uf_dest

            values['issqn_base'] += line.issqn_base_calculo
            values['issqn_value'] += abs(line.issqn_valor)

            values['ipi_base'] += line.ipi_base_calculo
            values['ipi_value'] += line.ipi_valor

            values['pis_base'] += line.pis_base_calculo
            values['pis_value'] += abs(line.pis_valor)

            values['cofins_base'] += line.cofins_base_calculo
            values['cofins_value'] += abs(line.cofins_valor)

            values['ii_value'] += line.ii_valor

            values['csll_base'] += line.csll_base_calculo
            values['csll_value'] += abs(line.csll_valor)

            values['irrf_base'] += line.irrf_base_calculo
            values['irrf_value'] += abs(line.irrf_valor)

            values['inss_base'] += line.inss_base_calculo
            values['inss_value'] += abs(line.inss_valor)
            values['inss_food_voucher'] += abs(line.inss_food_voucher)
            values['inss_transportation_voucher'] += abs(line.inss_transportation_voucher)  # noqa
            values['inss_tools_supplies'] += abs(line.inss_tools_supplies)

            if line.pis_valor < 0:
                values['pis_retention'] += line.pis_valor

            if line.cofins_valor < 0:
                values['cofins_retention'] += line.cofins_valor

            if line.csll_valor < 0:
                values['csll_retention'] += line.csll_valor

            if line.irrf_valor < 0:
                values['irrf_retention'] += line.irrf_valor

            if line.inss_valor < 0:
                values['inss_retention'] += line.inss_valor

            values['total_bruto'] += line.valor_bruto
            values['total_desconto'] += line.valor_desconto

            values['financial_price_total'] += line.financial_price_total

            values['total_tributos_federais'] += line.tributos_estimados_federais
            values['total_tributos_estaduais'] += line.tributos_estimados_estaduais
            values['total_tributos_municipais'] += line.tributos_estimados_municipais
            values['total_tributos_estimados'] += line.tributos_estimados

        values['inss_deduction_total'] = values['inss_food_voucher'] + values['inss_transportation_voucher'] + values['inss_tools_supplies']  # noqa

        # TOTAL
        values['amount_total'] = values['total_bruto'] - values['total_desconto'] + values['total_tax']  # noqa

        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1

        values['amount_total_company_signed'] = values['amount_total'] * sign
        values['amount_total_signed'] = values['amount_total'] * sign

        self.update(values)

    @api.onchange('discount_type', 'discount_rate', 'invoice_line_ids')
    def supply_rate(self):
        for inv in self:
            if inv.discount_rate != 0:
                if inv.discount_type == 'percent':
                    for line in inv.invoice_line_ids:
                        line.discount = inv.discount_rate
                        # Calculando o Valor dos Itens
                        line.onchange_br_account_discount()
                else:
                    total = discount = 0.0
                    for line in inv.invoice_line_ids:
                        total += round(line.quantity * line.price_unit_base, 2)

                    # Caso o total sej 0, manter o desconto como 0
                    if total > 0:
                        discount = round((inv.discount_rate / total) * 100, 2)

                    for line in inv.invoice_line_ids:
                        line.discount = discount
                        # Calculando o Valor dos Itens
                        line.onchange_br_account_discount()

                # Calculando o Valor total da Fatura
                inv._compute_amount()

    @api.multi
    @api.depends('custom_stage_id')
    def _compute_stage_color(self):
        """Método compute para popular o campo many2many
        custom_stage_color, nesse campo, que estárá como tag,
        o usuário poderá escolher a cor que deseja para o
        marcador.
        """
        for rec in self:
            if rec.custom_stage_id:
                rec.custom_stage_color = rec.custom_stage_id.stage_color_ids

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        """Sobrescreve onchange do core. Restaura o
        valor dos campos 'payment_term_id' e 'fiscal_position_id'
        em casos onde o parceiro não foi alterado mas o metodo
        onchange foi chamado (por exemplo, quando editamos
        algum campo do parceiro). Isso evita que valores inseridos
        em 'fiscal_position_id' e 'payment_term_id' selecionados
        pelo usuário sejam perdidos.

        Returns:
            dict -- domain das unidade utilizada pelo produto.
        """
        res = super(AccountInvoice, self)._onchange_partner_id()

        # O atributo '_origin' armazena o valor antigo de cada
        # campo da model
        if hasattr(self, '_origin') and self._origin.partner_id == self.partner_id:  # noqa
            values = {}
            if self._origin.payment_term_id:
                values['payment_term_id'] = self._origin.payment_term_id.id
            if self._origin.fiscal_position_id:
                values['fiscal_position_id'] = self._origin.fiscal_position_id.id  # noqa
            if self._origin.document_serie_id:
                values['document_serie_id'] = self._origin.document_serie_id.id

            if values:
                self.update(values)

        return res

    @api.onchange('issuer')
    def _onchange_issuer(self):
        if self.issuer == '0' and self.type in ('in_invoice', 'in_refund'):
            self.fiscal_document_id = None
            self.document_serie_id = None

    @api.onchange('fiscal_document_id')
    def _onchange_fiscal_document_id(self):
        """Metodo onchange base para ser implementados
        em outros modulos. O codigo original deste metodo
        foi removido pro gerar inconsistências quando mais de uma
        serie possuia o mesmo doc. fiscal .
        O metodo foi mantido aqui por questões de compatibilidade
        """
        pass

    def action_reload_fiscal_position_taxes(self):
        """Recarrega os impostos das linhas da fatura.
        Este método deve ser usado quando a posição fiscal
        é alterada tendo as linhas da fatura já sido preenchidas
        """
        if self.reload_taxes:
            self._onchange_br_account_fiscal_position_id()
            self._onchange_fiscal_document_id()
            self._onchange_journal_id()

            # Necessario para atualizar taxas de cada linha
            for line in self.invoice_line_ids:
                # enviamos a tag 'keep_price_unit' que sera usado no
                # metodo '_set_taxes' do core, para que o mesmo nao sobrescreva
                # o valor do campo 'price_unit'
                line.with_context(keep_price_unit=True)._set_taxes()
                line._set_extimated_taxes(line.price_subtotal)
                line._compute_price()

            # Como atualizamos os impostos das linhas
            # garantimos que a flag esteja desabilitada
            self.reload_taxes = False

    @api.onchange('fiscal_position_id')
    def _onchange_br_account_fiscal_position_id(self):
        """ Método para popular campos de acordo com a posição fiscal

        """
        if self.fiscal_position_id and self.fiscal_position_id.account_id:
            self.account_id = self.fiscal_position_id.account_id.id
        else:
            # Caso a posicao fiscal não tenha conta contabil, restauramos
            # a conta da fatura a partir da conta presente no cadastro
            # do parceiro
            rec_account = self.partner_id.property_account_receivable_id
            pay_account = self.partner_id.property_account_payable_id

            if self.type in ('in_invoice', 'in_refund'):
                self.account_id = pay_account.id
            else:
                self.account_id = rec_account.id

        if self.fiscal_position_id and self.fiscal_position_id.journal_id:
            self.journal_id = self.fiscal_position_id.journal_id
        else:
            # Caso a posicao fiscal nao possua diario contabil restauramos
            # o diario padrao utilizado na fatura caso não preenchido.
            if not self.journal_id:
                self.journal_id = self._default_journal()

        # Se for lançamento de Receitas ou Despesas Ignorar
        if not self._context.get('journal_type') in ('company_expense', 'company_revenue'):  # noqa
            ob_ids = [x.id for x in self.fiscal_position_id.fiscal_observation_ids]  # noqa

            self.update({
                'fiscal_observation_ids': [(6, False, ob_ids)],
                'fiscal_document_id': self.fiscal_position_id.fiscal_document_id.id,  # noqa
                'document_serie_id': self.fiscal_position_id.document_serie_id.id,  # noqa
                'fiscal_comment': self.fiscal_position_id.note,
                'reload_taxes': False if not self.invoice_line_ids or self.state != 'draft' else True,  # noqa
            })

    @api.onchange('partner_id', 'service_locale_address_id')
    def _onchange_service_locale_address_id(self):
        """Metodo onchange para o campo 'service_locale_address_id'
        """
        self.public_location = self.service_locale_address_id.public_location

    @api.multi
    def action_move_create(self):
        """ Cria lançamento de diario a partir da confirmação da fatura.
            Diferente do mesmo metodo presente no core, este metodo altera
            o comportamento original criando uma account.move para cada
            parcela do sistema e separando assim as account.move.line
            e lançamentos diferentes.
        """
        # O sistema de parcelas sera obrigatorio, entao sempre teremos pelo
        # menos uma parcela. Esse verificacao foi adicionada para manter
        # compatibilidade com os testes do core.
        # O valor 'user_parcel_system' foi adicionado no metodo
        # 'action_br_account_invoice_open'
        if not self.env.context.get('use_parcel_system') and not self.env.context.get('anticipated_payment'):  # noqa
            return super(AccountInvoice, self).action_move_create()

        for inv in self:
            if not inv.journal_id.sequence_id:
                raise UserError(_('Please define sequence on the journal related to this invoice.'))  # noqa

            if not inv.invoice_line_ids:
                raise UserError(_('Please create some invoice lines.'))

            ctx = dict(self._context, lang=inv.partner_id.lang)

            inv.with_context(ctx).write({
                'date_invoice': fields.Date.context_today(self),
            })

            company_currency = inv.company_id.currency_id

            # create move lines (one per invoice line + eventual taxes and
            #  analytic lines)
            iml = inv.invoice_line_parcel_get()

            # Montamos as move lines das taxas
            iml += inv.tax_line_move_line_get()

            # create one move line for the total and possibly adjust the other
            # lines amount
            iml = inv.with_context(ctx).compute_invoice_totals(company_currency, iml)[2]  # noqa

            # Filtrar as Parcelas que precisam ser geradas
            if self.env.context.get('anticipated_payment'):
                # Somente Gerar as Parcelas de Adiantamento
                generate_parcel_ids = inv.parcel_ids.filtered(lambda r: r.anticipated_payment and r.move_state == 'none')  # noqa
            else:
                # Somente Gerar as Parcelas sem ter gerado account_move
                generate_parcel_ids = inv.parcel_ids.filtered(lambda r: r.move_state == 'none')  # noqa

            # Para cada parcela criamos uma account.move, ou seja,
            # cada parcela gera um lançamento de diario
            for parcel in generate_parcel_ids:
                # Calculamos a nova data de vencimento baseado na data
                # de validação da faturação, caso a parcela nao esteja
                # marcada como 'data fixa'. A data da parcela também é
                # atualizada
                parcel.update_date_maturity(inv.date_invoice)

                # Realizamos um copia verdadeira do iml
                new_iml = copy.deepcopy(iml)

                # Fazemos o rateio do valor acordo com a percentagem
                # da parcela em relação ao total financeiro. Para garantir
                # que os valores das linhas da move.line sejam proporcionais
                # ao valor da parcela
                ratio = parcel.parceling_value / self.financial_price_total
                sum_in_previous_lines = 0
                dif_soma = 0

                for ml in new_iml:
                    # Fazemos o rateio do valor do imposto de acordo com a
                    # porcentagem da parcela em relação ao total financeiro.
                    # Garante que o valor do impostos e dois demais valores
                    # da move.line sejam proporcionais a parcela
                    ml['price'] = round(ml['price'] * ratio, 2)
                    ml['date_maturity'] = parcel.date_maturity

                    # Realizamos a soma dos valores para balancear uma possível
                    # diferença
                    sum_in_previous_lines += ml['price']

                # Força arrendamento para 2 casas
                sum_in_previous_lines = round(sum_in_previous_lines, 2)

                # Verificamos se houve sobra na dizima
                dif_soma = round(parcel.parceling_value - abs(sum_in_previous_lines), 2)  # noqa

                if dif_soma != 0:
                    if sum_in_previous_lines < 0:
                        # Inverter o sinal antes de adicionar a diferença
                        dif_soma *= -1

                    # Adicionando a diferença no primeiro item
                    new_iml[0]['price'] += dif_soma

                # Criamos a move line que ira balancear o total das
                # linhas de produto e taxas
                new_iml.append({
                    'type': 'dest',
                    'name': inv.name or '/',
                    'price': abs(sum_in_previous_lines + dif_soma) * parcel.signal,
                    'account_id': inv.account_id.id,
                    'date_maturity': parcel.date_maturity,
                    'amount_currency': parcel.amount_currency,
                    'currency_id': parcel.currency_id.id,
                    'invoice_id': inv.id,
                    'company_id': inv.company_id.id,
                })

                part = self.env['res.partner']._find_accounting_partner(inv.partner_id)  # noqa

                line = [(0, 0, self.line_get_convert(l, part.id)) for l in new_iml]  # noqa
                line = inv.group_lines(new_iml, line)

                journal = inv.journal_id.with_context(ctx)
                line = inv.finalize_invoice_move_lines(line)

                date = inv.date or inv.date_invoice

                move_vals = {
                    'date_maturity_current': parcel.date_maturity,
                    'date_maturity_origin': parcel.date_maturity,
                    'financial_operation_id': parcel.financial_operation_id.id,
                    'title_type_id': parcel.title_type_id.id,
                    'ref': inv.reference,
                    'line_ids': line,
                    'journal_id': journal.id,
                    'date': date,
                    'narration': inv.comment,
                    'parcel_id': parcel.id,
                    'company_id': inv.company_id.id,
                    'invoice_id': inv.id,
                    'amount_origin': parcel.parceling_value,
                    'account_group_id': inv.account_group_id.id,
                    'financial_identifier': inv.financial_identifier,
                }

                if inv.bank_account_for_expected:
                    move_vals['bank_account_for_expected'] = inv.bank_account_for_expected.id  # noqa

                ctx['company_id'] = inv.company_id.id
                ctx['invoice'] = inv

                ctx_nolang = ctx.copy()
                ctx_nolang.pop('lang', None)

                move = self.env['account.move'].with_context(ctx_nolang).create(move_vals)  # noqa

                # Pass invoice in context in method post:
                #   used if you want to get
                # the same account move reference when creating the
                #  same invoice after a cancelled one:
                move.post()

                if not self.env.context.get('anticipated_payment'):
                    # make the invoice point to that move
                    # Mantido por questao de compatibilidade
                    values = {
                        'move_id': move.id,
                        'date': date,
                        'move_name': move.name,
                        'number_backup': move.name,
                    }
                    inv.with_context(ctx).write(values)

        return True

    def get_locale_date(self, original_date):
        """Formata data para formatacao utilizado no Brasil.

            str -- data no formato dd-mm-aaaa
        """
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
        try:
            dt = original_date.strftime('%d/%m/%Y')
        except AttributeError:
            dt = ''

        return '{}'.format(dt)

    def _get_outstanding_info_JSON(self):
        """Sobrescrevemos metodo do core, e setamos a flag
        'has_outstanding' como False, para que a mensagem de pagamentos
        pendentes nunca seja exibida.
        """
        super(AccountInvoice, self)._get_outstanding_info_JSON()

        for inv in self:
            inv.has_outstanding = False

    @api.multi
    @api.depends('parcel_ids.date_maturity')
    def _compute_parcels_date_maturity(self):
        msg = ""

        for inv in self:

            for parcel in inv.parcel_ids:
                msg += str(self.get_locale_date(parcel.date_maturity)) + ", "

            inv.parcels_date_maturity = msg

    @api.depends('move_ids.amount_residual', 'move_ids.currency_id')
    def _compute_residual(self):
        """Realiza calculo do valore residual a ser pago da fatura.
        """
        for inv in self:
            # Quando a fatura nao possui parcela, ela utiliza
            # o financeiro do core (antigo)
            if not inv.parcel_ids:
                super(AccountInvoice, self)._compute_residual()
            else:
                # Se entrar aqui utilizamos o novo financeiro
                # o calculo do residual é realizado sobre as account.move
                # geradas pela parcela
                residual = 0.0
                residual_company_signed = 0.0

                # Obtemos o sinal do residual, dependendo do tipo da fatura
                sign = inv.type in ['in_refund', 'out_refund'] and -1 or 1

                # A diferenca do metodo original, e que aqui iremos percorrer
                # mais de uma account.move, uma vez que no novo financeiro
                # cada parcela gera uma account.move
                move_ids_cancel = all(l.paid_status == 'cancelled' for l in inv.sudo().move_ids)  # noqa

                if not move_ids_cancel:
                    for move in inv.sudo().move_ids:
                        if move.account_id == inv.account_id and move.paid_status != 'cancelled':  # noqa

                            residual_company_signed += move.amount_residual

                            # Caso account.move e a fatura ser da mesma moeda
                            if move.currency_id == inv.currency_id:
                                residual += move.amount_residual

                            else:
                                # Caso contrario, realizamos a conversao
                                from_currency = (move.currency_id and move.currency_id.with_context(date=move.date)) or move.company_id.currency_id.with_context(date=move.date)  # noqa

                                residual += from_currency._convert(
                                    from_amount=move.amount_residual,
                                    to_currency=move.currency_id,
                                    company=inv.company_id,
                                    date=move.date)

                inv.residual_company_signed = abs(residual_company_signed) * sign  # noqa
                inv.residual_signed = abs(residual) * sign
                inv.residual = abs(residual)

                # Verificamos se a fatura foi reconciliada quando o valor
                # residual e zero e os títulos não foram cancelados
                if not move_ids_cancel and float_is_zero(inv.residual, precision_rounding=inv.currency_id.rounding):  # noqa
                    inv.reconciled = True
                else:
                    inv.reconciled = False

    @api.multi
    def action_generate_anticipated_payment(self):
        """ Metodo criado para

        :return: True se o record foi salvo e False, caso contrário.
        """
        self.ensure_one()

        if self.parcel_ids and self.anticipated_residual_value > 0:

            self.validate_date_maturity_from_parcels()

            if self.compare_total_parcel_value():
                self.with_context(anticipated_payment=True).action_move_create()  # noqa
            else:
                raise UserError(_('O valor total da fatura e total das '
                                  'parcelas divergem! Por favor, gere as '
                                  'parcelas novamente.'))
        else:
            raise ValidationError('Campo parcela está vazio ou não existe(m) parcela(s) a antecipar')  # noqa

    @api.multi
    def action_open_periodic_entry_wizard(self):
        """Abre wizard para gerar pagamentos periodicos"""
        self.ensure_one()

        date_invoice = None

        if self.type in ('out_invoice', 'out_refund'):
            date_invoice = self.pre_invoice_date

        if self.type in ('in_invoice', 'in_refund'):
            date_invoice = self.date_invoice

        if not date_invoice:
            raise UserError('Nenhuma data fornecida como base para a criação das parcelas!')  # noqa

        if self.state != 'draft':
            raise UserError('Parcelas podem ser criadas apenas quando a '
                            'fatura estiver como "Provisório"')

        if not self.payment_term_id:
            raise UserError('Nenhuma condição de pagamento foi fornecida. Por'
                            'favor, selecione uma condição de pagamento')

        if not self.invoice_line_ids:
            raise UserError('Nenhuma linha de fatura foi fornecida. Por '
                            'favor insira ao menos um produto/serviço')

        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'br_account.invoice.parcel.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'context': {
                'default_payment_term_id': self.payment_term_id.id,
                'default_pre_invoice_date': date_invoice,
            },
            'views': [(False, 'form')],
            'target': 'new',
        }

        return action

    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        self.action_number()
        return res

    @api.multi
    def action_invoice_draft(self):

        for invoice in self:

            if invoice.position_type == 'service':

                invoice.invoice_line_ids.write({
                    'pis_ignore_amount': True,
                    'cofins_ignore_amount': True,
                    'irrf_ignore_amount': True,
                    'csll_ignore_amount': True,
                })

        return super(AccountInvoice, self).action_invoice_draft()

    @api.multi
    def br_account_invoice_confirm_in_queue(self):
        """Metodo para realização da confirmação em lote da fatura pela queue.
        O uso do sudo() se faz necessario para que não ocorra erros de permissão de
        leitura quando o usuario estiver logado em uma empresa diferente da empresa
        que gerou a fatura na queue.
        """

        for inv in self:

            company = inv.sudo().company_id

            # Repassando o usuário para gravar o log corretamente
            user_id = self._context.get('uid', self.env.user.id)

            inv.sudo().with_context(force_company=company, force_uid_log=user_id).action_br_account_invoice_open()  # noqa

    @api.multi
    def _hook_validation(self):
        """Valida dados da fatura, retornando uma lista
        com as mensagens de err

        Returns:
        boolean: Caso a validação seja bem sucedida
        """

        if not self.parcel_ids:
            raise ValidationError('Campo parcela está vazio. Por favor, crie as parcelas')  # noqa

        if self.state == 'blocked':
            raise ValidationError(_('Invoice is blocked, check the reasons.'))  # noqa

        if self.reload_taxes:
            raise ValidationError('A Posição Fiscal foi alterada! Por favor, recarrega os impostos antes de continuar.')  # noqa

        # Adiciona Verificação para Evitar Erros nas Contas
        if self.journal_id.type in ('sale', 'purchase'):

            d1 = (self.type == 'in_invoice' and (self.account_id.internal_type != 'payable' or self.account_id.code_first_digit != '2'))  # noqa
            d2 = (self.type == 'out_invoice' and (self.account_id.internal_type != 'receivable' or self.account_id.code_first_digit != '1'))  # noqa

            if d1 or d2:
                raise ValidationError(_('Account selected for this invoice is invalid for this invoice type.'))  # noqa

        if self.parcel_ids.filtered(lambda r: r.anticipated_payment):

            anticipated_paid = 0

            for parcel in self.parcel_ids:

                for move in parcel.move_ids.filtered(lambda r: r.paid_status in ('paid', 'partial')):
                    anticipated_paid += move.amount - move.amount_residual

            if self.anticipated_value != anticipated_paid:
                raise ValidationError(_('It is not possible to confirm the Invoice as there are outstanding advance amounts to be received.'))  # noqa

        self.validate_date_maturity_from_parcels()

        if not self.lock_checks():
            return False

        if not self.compare_total_parcel_value():
            raise UserError(_('O valor total da fatura e total das parcelas divergem! Por favor, gere as parcelas novamente.'))  # noqa

        return True

    @api.multi
    def action_br_account_invoice_open(self):
        """Metodo criado para manter a compatibilidade dos testes do core
        com o sistema de criação de parcelas do br_account. Anteriormente
        o metodo 'action_invoice_open' era chamado ao clicar no botao 'Validar'
        da Fatura. Este metodo realiza a verificacao das parcelas ao mesmo
        tempo que permite compatibilidade com os testes do core

        :return: True se o record foi salvo e False, caso contrário.
        """
        # Validamos os dados da invoice
        if self._hook_validation():

            # Ajustamos os valores dos impostos (detalhes no doc. do metodo)
            self.action_br_account_invoice_recompute_tax()

            return super(AccountInvoice, self).with_context(use_parcel_system=True).action_invoice_open()  # noqa

        else:
            return False

    @api.multi
    def action_number(self):

        for invoice in self:
            if invoice.fiscal_document_id:

                if not invoice.document_serie_id:
                    raise UserError('Configure uma série para a fatura')  # noqa

                elif not invoice.document_serie_id.internal_sequence_id:
                    raise UserError('Configure a sequência para a numeração da nota')  # noqa

            if invoice.document_serie_id:

                if invoice.type == 'in_invoice' and invoice.vendor_number:
                    seq_number = invoice.vendor_number
                else:
                    seq_number = invoice.document_serie_id.internal_sequence_id.next_by_id()  # noqa: 501

                    # Percorremos cada uma das faturas de modo a verificar se o numero
                    # ja nao foi utilizado por outra fatura com o mesmo doc. fiscal
                    # Para NFe de Servico, isso nao se aplica porque o numero interno
                    # e utilizado para gerar o RPS sendo o numero da fatura (RPS convertido em NFe)
                    # fornecido pela consulta na prefeitura
                    if invoice.document_serie_id.fiscal_document_id.code != '001':

                        while True:

                            domain = [
                                ('internal_number', '=', seq_number),
                                ('document_serie_id', '=',
                                 invoice.document_serie_id.id),
                            ]

                            if not self.env['account.invoice'].search(domain):
                                break
                            else:
                                seq_number = invoice.document_serie_id.internal_sequence_id.next_by_id()  # noqa: 501

                invoice.internal_number = seq_number

        return True

    @api.multi
    def compare_total_parcel_value(self):

        # Obtemos o total dos valores da parcela
        total = sum([p.parceling_value for p in self.parcel_ids])

        # Obtemos a precisao configurada
        prec = self.env['decimal.precision'].precision_get('Account')

        # Comparamos o valor total da invoice e das parcelas
        # a fim de verificar se os valores sao os mesmos
        # float_compare retorna 0, se os valores forem iguais
        # float_compare retorna -1, se amount_total for menor que total
        # float_compare retorna 1, se amount_total for maior que total
        if float_compare(self.financial_price_total, total, precision_digits=prec):
            return False
        else:
            return True

    @api.multi
    def validate_date_maturity_from_parcels(self):
        """Verifica se algum registro no campo parcel_ids tem data de
        vencimento menor que o campo pre_invoice_date da fatura.

        Raises:
            UserError -- Ao menos uma parcela gerada tem data de vencimento
            menor que a data de pré fatura.
        """
        for inv in self:

            if inv.journal_id.type == 'sale':

                has_incoerent_parcel = any(parcel.date_maturity < inv.pre_invoice_date for parcel in inv.parcel_ids)  # noqa

                if has_incoerent_parcel:
                    raise UserError(_('Pelo menos um registro de parcela foi criado com '
                                      'data de vencimento menor do que a data da '
                                      'pré-fatura, por favor, considere verificar o campo '
                                      'payment_term_id'))

    @api.multi
    def action_invoice_cancel_paid(self):
        if self.filtered(lambda inv: inv.state not in ['proforma2', 'draft', 'open', 'paid']):  # noqa
            raise UserError(_("Invoice must be in draft, Pro-forma or open state in order to be cancelled."))  # noqa

        return self.action_cancel()

    @api.multi
    def action_cancel(self):
        """Sobrescrita do metodo de cancelamento da Fatura.
        Remove as account.move acopladas a fatura quando a mesma
        e confirmada. Foi necessario sobrescrever o metodo do
        core porque a fatura agora gera uma account.move por
        parcela (após correções no financeiro).

        Raises:
            UserError -- Quando a fatura esta parcialmente paga.

        Returns:
            bool -- True quando o metodo foi executado sem erro.
        """
        moves = self.env['account.move']

        for inv in self:

            # Quando a fatura nao possui parcela, ela utiliza
            # o financeiro do core (antigo)
            if not inv.parcel_ids:
                return super(AccountInvoice, self).action_cancel()
            else:
                if inv.move_ids:
                    moves += inv.move_ids

                if any(move for move in inv.move_ids if move.paid_status == 'partial'):
                    raise UserError(
                        _('You cannot cancel an invoice which is partially paid.'
                          'You need to unreconcile related payment entries first.'))

        # Inicialmente, alteramos o status da fatura para 'cancel' e
        # desacoplamos as move_ids.
        # Apagamos o valor da data de confirmacao para que a geracao da
        # parcela continue consistente
        self.write({
            'state': 'cancel',
            'move_ids': False,
            'move_id': False,
            'cancel_invoice_date': fields.Date.today(),
        })

        if moves:
            # segundo, invalidamos as move(s)
            moves.button_cancel()

            # Excluimos as moves desta invoice estava apontando.
            # As move.lines e move.reconciles correspondentes serao automaticamente
            # excluidas tambem.
            moves.unlink()
        return True

    @api.model
    def invoice_line_parcel_get(self):
        """ Metodo monta valores da parcela
            baseado no retorno do metodo 'invoice_line_move_line_get'.
            A unica diferença aqui é que o valor usado é total financeiro.

        Returns:
            dict: Conjunto de valores para calculo do valor das parcelas
        """
        res = super(AccountInvoice, self).invoice_line_move_line_get()

        for index, line in enumerate(self.invoice_line_ids):
            res[index]['analytic_type_id'] = line.analytic_type_id.id if line.analytic_type_id else False  # noqa
            if line.quantity != 0:
                res[index]['price'] = line.financial_price_total

        return res

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):

        res = super(AccountInvoice, self).finalize_invoice_move_lines(move_lines)  # noqa

        count = 1

        for invoice_line in res:
            line = invoice_line[2]
            line['ref'] = self.origin
            # Corrige a gravação do Parceiro original da Invoice
            line['partner_id'] = self.partner_id.id

            if line['name'] == '/' or (line['name'] == self.name and self.name):  # noqa
                line['name'] = "%02d" % count
                count += 1

        return res

    def _prepare_tax_line_vals(self, line, tax):
        """ Prepare values to create an account.invoice.tax line

        The line parameter is an account.invoice.line, and the
        tax parameter is the output of account.tax.compute_all().
        """
        vals = super(AccountInvoice, self)._prepare_tax_line_vals(line=line, tax=tax)  # noqa

        if 'amount_original' in tax:
            vals['amount_original'] = tax['amount_original']

        if 'minimal_value' in tax:
            vals['minimal_value'] = tax['minimal_value']

        return vals

    @api.multi
    def get_taxes_values(self):
        tax_grouped = {}

        round_curr = self.currency_id.round

        for line in self.invoice_line_ids:

            other_taxes = line.invoice_line_tax_ids.filtered(lambda x: not x.domain)  # noqa

            line.invoice_line_tax_ids = (other_taxes |
                                         line.tax_icms_id |
                                         line.tax_ipi_id |
                                         line.tax_pis_id |
                                         line.tax_cofins_id |
                                         line.tax_issqn_id |
                                         line.tax_ii_id |
                                         line.tax_icms_st_id |
                                         line.tax_simples_id |
                                         line.tax_csll_id |
                                         line.tax_irrf_id |
                                         line.tax_inss_id)

            ctx = line._prepare_tax_context()
            tax_ids = line.invoice_line_tax_ids.with_context(**ctx)

            taxes = tax_ids.compute_all(line.price_unit, self.currency_id, line.quantity,
                                        line.product_id, self.partner_id)['taxes']

            for tax in taxes:

                val = self._prepare_tax_line_vals(line, tax)
                key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)  # noqa

                if key not in tax_grouped:
                    tax_grouped[key] = val
                    tax_grouped[key]['base'] = round_curr(val['base'])
                else:
                    tax_grouped[key]['amount'] += val['amount']

                    if 'amount_original' in val:
                        tax_grouped[key]['amount_original'] += val['amount_original']

                    tax_grouped[key]['base'] += round_curr(val['base'])

        # Vericamos se a soma dos valores de cada imposto e maior
        # que seu valor minimo
        for _, tax in tax_grouped.items():

            tax_obj = self.env['account.tax'].browse(tax['tax_id'])  # noqa

            if self.position_type == 'service' and ('amount_original' in tax and abs(tax['amount_original']) >= abs(tax_obj.minimal_value)):  # noqa
                tax['amount'] = tax['amount_original']

            if not tax_obj.price_include:
                tax['invoice_price_total'] = round_curr(tax['amount'])
            else:
                tax['invoice_price_total'] = 0

            if tax_obj.price_include and tax_obj.include_parcel_total:
                tax['financial_price_total'] = round_curr(tax['amount'])
            else:
                tax['financial_price_total'] = 0

        return tax_grouped

    @api.model
    def tax_line_move_line_get(self):
        """Retorna valores utilizados para criação das
        move lines que representam as taxas. Cria novas
        entradas apenas para taxas que não são somandas
        no preço do produto.

        Returns:
            list -- lista com dict de campos das move lines.
        """
        res = super(AccountInvoice, self).tax_line_move_line_get()

        done_taxes = []

        for tax_line in sorted(self.tax_line_ids, key=lambda x: -x.sequence):

            tax = tax_line.tax_id

            # Somente para taxas que são incluidas no preço.
            # Quando as taxas são incluidas no preço e nao sao somandos ao total financeiro, e necessario
            # criar uma nova move line para balancea-la. Omitir 'deduced_account_id' pode causar criação
            # de move lines sem account_id
            if tax_line.amount and (tax.price_include and not tax.include_parcel_total) and tax.deduced_account_id:  # noqa

                done_taxes.append(tax.id)

                res.append({
                    'invoice_tax_line_id': tax_line.id,
                    'tax_line_id': tax_line.tax_id.id,
                    'type': 'tax',
                    'name': tax_line.name,
                    'price_unit': tax_line.amount * -1,
                    'quantity': 1,
                    'price': tax_line.amount * -1,
                    'account_id': tax_line.tax_id.deduced_account_id.id,
                    'account_analytic_id': tax_line.account_analytic_id.id,
                    'invoice_id': self.id,
                    'tax_ids': [(6, 0, done_taxes)] if tax_line.tax_id.include_base_amount else []  # noqa
                })

        return res

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):  # noqa

        res = super(AccountInvoice, self)._prepare_refund(
            invoice,
            date_invoice=date_invoice,
            date=date,
            description=description,
            journal_id=journal_id,
        )

        res['fiscal_document_id'] = invoice.fiscal_document_id.id
        res['document_serie_id'] = invoice.document_serie_id.id

        return res

    @api.multi
    def generate_parcel_entry(self, financial_operation, title_type, payment_term_id=False, parcel_total_value=0, parcel_unlink=True):
        """Cria as parcelas da fatura.
        """
        for inv in self:

            ctx = dict(self._context, lang=inv.partner_id.lang)

            date_invoice = None

            # Se não for enviado payment term, pegar da invoice
            if not payment_term_id:
                payment_term_id = inv.payment_term_id

            if inv.type in ('out_invoice', 'out_refund'):
                date_invoice = inv.pre_invoice_date

            if inv.type in ('in_invoice', 'in_refund'):
                date_invoice = inv.date_invoice

            if not date_invoice:
                raise UserError('Nenhuma data fornecida como base para a criação das parcelas!')  # noqa

            if inv.state != 'draft':
                raise UserError('Parcelas podem ser criadas apenas quando a '
                                'fatura estiver como "Provisório"')

            if not payment_term_id:
                raise UserError(
                    'Nenhuma condição de pagamento foi fornecida. Por'
                    'favor, selecione uma condição de pagamento')

            if not inv.invoice_line_ids:
                raise UserError('Nenhuma linha de fatura foi fornecida. Por '
                                'favor insira ao menos um produto/serviço')

            company_currency = inv.company_id.currency_id

            # create move lines (one per invoice line + eventual taxes and
            # analytic lines)
            iml = inv.invoice_line_parcel_get()

            diff_currency = inv.currency_id != company_currency

            total, total_currency, iml = inv.with_context(ctx).compute_invoice_totals(company_currency, iml)  # noqa

            # Caso tenha enviado o valor da parcela, assumir para os calculos
            if parcel_total_value > 0:
                total = total_currency = parcel_total_value

            aux = payment_term_id.with_context(**ctx, currency_id=company_currency.id).compute(total, date_invoice)  # noqa

            # Força Ordem de Data nas Parcelas
            lines_no_taxes = sorted(aux[0], key=lambda tup: (tup[0], tup[1]), reverse=False)  # noqa

            res_amount_currency = total_currency
            ctx['date'] = date_invoice

            if parcel_unlink:
                # Removemos as parcelas adicionadas anteriormente
                inv.parcel_ids.unlink()
                p_init = 0
            else:
                p_init = len(inv.parcel_ids)

            for i, t in enumerate(lines_no_taxes):
                if inv.currency_id != company_currency:
                    amount_currency = company_currency.with_context(ctx)._convert(t[1], inv.currency_id, inv.company_id, inv.pre_invoice_date)  # noqa
                else:
                    amount_currency = False

                # last line: add the diff
                res_amount_currency -= amount_currency or 0

                if i + 1 == len(lines_no_taxes):
                    amount_currency += res_amount_currency

                # Calculamos o valor da parcela
                parceling_value = round(t[1], 2)

                # Obtemos o sinal do residual, dependendo do tipo da fatura
                sign = 1 if parceling_value >= 0 else -1

                values = {
                    'name': str(i + p_init + 1).zfill(2),
                    'parceling_value': abs(parceling_value),
                    'signal': sign,
                    'date_maturity': t[0],
                    'old_date_maturity': t[0],
                    'financial_operation_id': financial_operation.id,
                    'title_type_id': title_type.id,
                    'amount_currency': diff_currency and amount_currency,
                    'currency_id': diff_currency and inv.currency_id.id,
                    'invoice_id': inv.id,
                }

                self.env['br_account.invoice.parcel'].create(values)

        return True

    @api.model
    def line_get_convert(self, line, part):
        ret = super(AccountInvoice, self).line_get_convert(line, part)

        ret['title_type_id'] = line.get('title_type_id')
        ret['financial_operation_id'] = line.get('financial_operation_id')
        ret['analytic_type_id'] = line.get('analytic_type_id')

        return ret

    @api.multi
    def action_br_account_invoice_recompute_tax(self):
        """Quando o valor de um ou mais impostos ultrapassa o seu
        respectivo valor minimo, nos recalculamos todos os impostos
        e atualizamos o valor das parcelas de modo a tornar os valores
        da fatura consistente.
        """

        for inv in self:

            if inv.position_type == 'service' and inv.state in ('draft', '':

                # Calculos realizados a partir da tax_line devido a sitacoes de
                # calculo de valor minimo e tambem para evitar recalcular o
                # o total desses impostos
                pis = inv.tax_line_ids.filtered(lambda r: r.tax_id.domain == 'pis')  # noqa
                cofins = inv.tax_line_ids.filtered(lambda r: r.tax_id.domain == 'cofins')  # noqa
                csll = inv.tax_line_ids.filtered(lambda r: r.tax_id.domain == 'csll')  # noqa
                irrf = inv.tax_line_ids.filtered(lambda r: r.tax_id.domain == 'irrf')  # noqa

                # Se tax.amount_total for maior que zero, significa que
                # no total, o imposto ultrapassou seu referido valor minimo
                pis_value = sum(abs(tax.amount_total) for tax in pis)
                cofins_value = sum(abs(tax.amount_total) for tax in cofins)
                csll_value = sum(abs(tax.amount_total) for tax in csll)
                irrf_value = sum(abs(tax.amount_total) for tax in irrf)

                pis_ignore_amount = False if pis_value else True
                cofins_ignore_amount = False if cofins_value else True
                irrf_ignore_amount = False if irrf_value else True
                csll_ignore_amount = False if csll_value else True

                inv.invoice_line_ids.write({
                    'pis_ignore_amount': pis_ignore_amount,
                    'cofins_ignore_amount': cofins_ignore_amount,
                    'irrf_ignore_amount': irrf_ignore_amount,
                    'csll_ignore_amount': csll_ignore_amount,
                })

                if not pis_ignore_amount or not cofins_ignore_amount or not irrf_ignore_amount or not csll_ignore_amount:

                    # Salvamos o atual total financeiro antes de o recalcularmos
                    old_financial_price_total = inv.financial_price_total

                    # Atualizamos os valores das linhas ja que os impostos tiveram de ser recalculados
                    inv.invoice_line_ids._compute_price()

                    # Atualizamos o total da fatura
                    inv._compute_amount()

                    for parc in inv.parcel_ids:

                        # Calculamos a razao entre a parcela e o total financeiro antigo
                        ratio = parc.parceling_value / old_financial_price_total

                        # Calculamos o novo valor da parcela a partir do novo total financeiro
                        # e da razao da parcela. Fazemos isso porque pode haver casos
                        # onde as parcelas possuem valores diferentes
                        parc.parceling_value = inv.financial_price_total * ratio

    def toggle_blocked(self, unlock_state='draft'):
        """ Sobscreve o metodo ajustando o unlock_state

        Args:
            unlock_state (str): State do desbloqueio de acordo
             com os move_ids: Gerado == Open ou == Draft
        """
        if self.move_ids:
            unlock_state = 'open'
        else:
            unlock_state = 'draft'

        super(AccountInvoice, self).toggle_blocked(unlock_state=unlock_state)
