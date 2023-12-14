# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    deduced_account_id = fields.Many2one('account.account',
                                         string="Conta de Dedução da Venda")

    refund_deduced_account_id = fields.Many2one('account.account',
                                                string="Conta de Dedução do Reembolso")

    domain = fields.Selection([('icms', 'ICMS'),
                               ('icmsst', 'ICMS ST'),
                               ('simples', 'Simples Nacional'),
                               ('pis', 'PIS'),
                               ('cofins', 'COFINS'),
                               ('ipi', 'IPI'),
                               ('issqn', 'ISSQN'),
                               ('ii', 'II'),
                               ('icms_inter', 'Difal - Alíquota Inter'),
                               ('icms_intra', 'Difal - Alíquota Intra'),
                               ('fcp', 'FCP'),
                               ('csll', 'CSLL'),
                               ('irrf', 'IRRF'),
                               ('inss', 'INSS'),
                               ('outros', 'Outros')],
                              string="Tipo")

    amount_type = fields.Selection(selection_add=[('icmsst', 'ICMS ST')])

    include_parcel_total = fields.Boolean(string='Incluido no Total da Parcela',
                                          help="Marque se o imposto deve ser somado ao total financeiro, de onde as parcelas serão geradas.")

    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Company Currency", readonly=True)

    minimal_value = fields.Monetary(string='Valor Mínimo',
                                    default=0,
                                    currency_field='company_currency_id',
                                    help='Valor minimo para pagamento do importo')

    @api.onchange('price_include')
    def onchange_price_include(self):
        super(AccountTax, self).onchange_price_include()

        if not self.price_include:
            self.include_parcel_total = False

    @api.onchange('include_parcel_total')
    def _onchange_include_parcel_total(self):

        if self.include_parcel_total:
            self.price_include = True

    @api.onchange('domain')
    def _onchange_domain_tax(self):
        if self.domain in ('icms', 'simples', 'pis', 'cofins', 'issqn', 'ii',
                           'icms_inter', 'icms_intra', 'fcp'):
            self.price_include = True
            self.amount_type = 'division'

        if self.domain in ('icmsst', 'ipi'):
            self.price_include = False
            self.include_base_amount = False
            self.amount_type = 'division'

        if self.domain == 'icmsst':
            self.amount_type = 'icmsst'

    @api.onchange('deduced_account_id')
    def _onchange_deduced_account_id(self):
        self.refund_deduced_account_id = self.deduced_account_id

    def _tax_vals(self, tax):
        return {
            'id': tax.id,
            'name': tax.name,
            'minimal_value': tax.minimal_value,
            'sequence': tax.sequence,
            'account_id': tax.account_id.id,
            'refund_account_id': tax.refund_account_id.id,
            'analytic': tax.analytic,
            'include_parcel_total': tax.include_parcel_total,
        }

    def _check_tax_minimal_value(self, tax, vals, ignore_amount=True):
        """Em notas de servico, os impostos PIS, COFINS, IRRF e CSLL
        que nao ultrapassarem o valor minimo (definido no cadastro do imposto)
        nao sao considerados na nota.

        Args:
            tax (account.tax): Taxa que sera analisada
            vals (dict): dict contendo valores pertinentes a serem retornados pelo imposto
            ignore_amount (bool, optional): Flag para forcar a verificacao e calculo do imposto. Defaults to True.

        Returns:
            dict: conteudo de `vals` atualizado com novo valor do imposto
        """

        position_type = self.env.context.get('position_type', False)

        # Regras para empresa no lucro presumido
        if position_type == 'service' and ignore_amount and abs(vals['amount']) < tax.minimal_value and tax.domain in ('pis', 'cofins', 'irrf', 'csll'):
            vals['amount'] = 0

        return vals

    def _compute_ipi(self, price_base, currency_id):
        ipi_tax = self.filtered(lambda x: x.domain == 'ipi')

        if not ipi_tax:
            return []

        vals = self._tax_vals(ipi_tax)

        reducao_ipi = self.env.context.get('ipi_reducao_bc', 0.0)

        base_ipi = price_base

        base_ipi += currency_id.round(self.env.context.get('valor_frete', 0))
        base_ipi += currency_id.round(self.env.context.get('valor_seguro', 0))
        base_ipi += currency_id.round(self.env.context.get('outras_despesas', 0))

        base_tax = base_ipi * (1 - (reducao_ipi / 100.0))

        # O IPI é do porcentagem, entao o valor dele ja e arredondado
        # pelo metodo da classe mae
        vals['amount'] = ipi_tax._compute_amount(base_tax, 1.0)
        vals['base'] = base_tax

        return [vals]

    def _compute_icms(self, price_base, ipi_value, currency_id):
        icms_tax = self.filtered(lambda x: x.domain == 'icms')

        if not icms_tax:
            return []

        # Obtendo Context
        incluir_ipi = self.env.context.get('incluir_ipi_base', False)
        reducao_icms = self.env.context.get('icms_aliquota_reducao_base', 0)
        service_locale = self.env.context.get('service_locale', False)
        icms_tax_locale = self.env.context.get('icms_tax_locale', False)
        ignore_icms_tax_locale = self.env.context.get('ignore_icms_tax_locale', False)  # noqa
        icms_cst_normal = self.env.context.get('icms_cst_normal', False)
        icms_csosn_simples = self.env.context.get('icms_csosn_simples', False)
        icms_cst = self.env.context.get('icms_cst', False)
        invoice_type = self.env.context.get('type', False)
        journal_type = self.env.context.get('journal_type', False)

        vals = self._tax_vals(icms_tax)
        base_icms = price_base

        if incluir_ipi:
            base_icms += ipi_value

        base_icms += currency_id.round(self.env.context.get('valor_frete', 0))
        base_icms += currency_id.round(self.env.context.get('valor_seguro', 0))
        base_icms += currency_id.round(self.env.context.get('outras_despesas', 0))
        base_icms *= 1 - (reducao_icms / 100.0)

        # Caso seja NF de Remessa ou NFE de Devolução para Fornecedor: Tem que ter base e ICMS
        if invoice_type == 'in_refund' and journal_type in ('purchase', 'simples_remessa'):
            vals['base'] = base_icms
            vals['amount'] = currency_id.round(icms_tax._compute_amount(base_icms, 1.0))

        else:
            # Base de calculo deve ser zerada quando cliente é isento
            # ou cliente pertence ao simples nacional (não valido para nota de devolução)
            if icms_cst_normal in ('30', '40', '41', '50', '60') or (icms_cst and icms_cst == icms_csosn_simples):
                vals['base'] = base_icms = 0
            else:
                vals['base'] = base_icms

            if ignore_icms_tax_locale:
                vals['amount'] = currency_id.round(icms_tax._compute_amount(base_icms, 1.0))

            elif service_locale and icms_tax_locale and icms_tax_locale in ('0', service_locale):
                vals['amount'] = currency_id.round(icms_tax._compute_amount(base_icms, 1.0))

            else:
                vals['amount'] = 0

        return [vals]

    def _compute_icms_st(self, price_base, ipi_value, icms_value, currency_id):
        icmsst_tax = self.filtered(lambda x: x.domain == 'icmsst')

        if not icmsst_tax:
            return []

        vals = self._tax_vals(icmsst_tax)

        base_icmsst = price_base + ipi_value

        invoice_type = self.env.context.get('type', False)
        journal_type = self.env.context.get('journal_type', False)
        reducao_icmsst = self.env.context.get('icms_st_aliquota_reducao_base', 0)  # noqa
        aliquota_mva = self.env.context.get('icms_st_aliquota_mva', 0)
        service_locale = self.env.context.get('service_locale', False)
        icms_tax_locale = self.env.context.get('icms_tax_locale', False)
        ignore_icms_tax_locale = self.env.context.get('ignore_icms_tax_locale', False)  # noqa
        icms_cst_normal = self.env.context.get('icms_cst_normal', False)
        icms_csosn_simples = self.env.context.get('icms_csosn_simples', False)
        icms_cst = self.env.context.get('icms_cst', False)

        base_icmsst += currency_id.round(self.env.context.get('valor_frete', 0))
        base_icmsst += currency_id.round(self.env.context.get('valor_seguro', 0))
        base_icmsst += currency_id.round(self.env.context.get('outras_despesas', 0))

        base_icmsst *= 1 - (reducao_icmsst / 100.0)  # Redução

        deducao_st_simples = self.env.context.get('icms_st_aliquota_deducao', 0)  # noqa

        if deducao_st_simples:
            icms_value = base_icmsst * (deducao_st_simples / 100.0)

        base_icmsst *= 1 + aliquota_mva / 100.0  # Aplica MVA

        icmsst = currency_id.round((base_icmsst * (icmsst_tax.amount / 100.0)) - icms_value)  # noqa

        # Caso seja NF de Remessa para Fornecedor: Tem que ter base e ICMS
        if invoice_type == 'in_refund' and journal_type == 'purchase':
            vals['amount'] = icmsst
            vals['base'] = base_icmsst
        else:
            if ignore_icms_tax_locale:
                vals['amount'] = icmsst if icmsst >= 0.0 else 0.0

            elif service_locale and icms_tax_locale and icms_tax_locale in ('0', service_locale):
                vals['amount'] = icmsst if icmsst >= 0.0 else 0.0

            else:
                vals['amount'] = 0

            # Base de calculo deve ser zerada quando cliente é isento
            # ou cliente pertence ao simples nacional
            if icms_cst_normal in ('30', '40', '41', '50') or (icms_cst and icms_cst == icms_csosn_simples):
                vals['base'] = 0
            else:
                vals['base'] = base_icmsst

        return [vals]

    def _compute_difal(self, price_base, ipi_value, currency_id):

        icms_inter = self.filtered(lambda x: x.domain == 'icms_inter')
        icms_intra = self.filtered(lambda x: x.domain == 'icms_intra')
        icms_fcp = self.filtered(lambda x: x.domain == 'fcp')

        if not icms_inter or not icms_intra:
            return []

        vals_inter = self._tax_vals(icms_inter)
        vals_intra = self._tax_vals(icms_intra)

        vals_fcp = self._tax_vals(icms_fcp) if icms_fcp else None

        base_icms = price_base + ipi_value

        reducao_icms = self.env.context.get('icms_aliquota_reducao_base', 0)

        base_icms += currency_id.round(self.env.context.get('valor_frete', 0))
        base_icms += currency_id.round(self.env.context.get('valor_seguro', 0))
        base_icms += currency_id.round(self.env.context.get('outras_despesas', 0))

        base_icms *= 1 - (reducao_icms / 100.0)

        interestadual = currency_id.round(icms_inter._compute_amount(base_icms, 1.0))
        interno = currency_id.round(icms_intra._compute_amount(base_icms, 1.0))

        vals_inter['amount'] = (interno - interestadual) * 0.0
        vals_inter['base'] = base_icms

        vals_intra['amount'] = (interno - interestadual) * 1.0
        vals_intra['base'] = base_icms

        taxes = [vals_inter, vals_intra]

        if vals_fcp:
            vals_fcp['amount'] = currency_id.round(icms_fcp._compute_amount(base_icms, 1.0))
            vals_fcp['base'] = base_icms
            taxes += [vals_fcp]

        return taxes

    def _compute_simples(self, price_base, currency_id):
        simples_tax = self.filtered(lambda x: x.domain == 'simples')

        if not simples_tax:
            return []

        taxes = []

        for tax in simples_tax:
            vals = self._tax_vals(tax)
            vals['amount'] = currency_id.round(tax._compute_amount(price_base, 1.0))
            vals['base'] = price_base
            taxes.append(vals)

        return taxes

    def _compute_pis_cofins(self, price_base, icms_value, currency_id):
        pis_cofins_tax = self.filtered(lambda x: x.domain in ('pis', 'cofins'))

        if not pis_cofins_tax:
            return []

        taxes = []

        service_locale = self.env.context.get('service_locale', False)
        pis_tax_locale = self.env.context.get('pis_tax_locale', False)
        cofins_tax_locale = self.env.context.get('cofins_tax_locale', False)

        pis_ignore_amount = self.env.context.get('pis_ignore_amount', False)
        cofins_ignore_amount = self.env.context.get('cofins_ignore_amount', False)

        deduzir_icms_base_pis = self.env.context.get('deduzir_icms_base_pis', False)
        deduzir_icms_base_cofins = self.env.context.get('deduzir_icms_base_cofins', False)

        for tax in pis_cofins_tax:
            vals = self._tax_vals(tax)

            new_price_base = price_base
            tax_locale = False

            if tax.domain == 'pis':
                tax_locale = pis_tax_locale
                ignore_amount = pis_ignore_amount

                if deduzir_icms_base_pis:
                    new_price_base -= icms_value

            if tax.domain == 'cofins':
                tax_locale = cofins_tax_locale
                ignore_amount = cofins_ignore_amount

                if deduzir_icms_base_cofins:
                    new_price_base -= icms_value

            # O calculo do imposto depende se o serviço foi
            # prestado dentro ou fora do municipio
            if service_locale and tax_locale and tax_locale in ('0', service_locale):
                vals['amount'] = currency_id.round(tax._compute_amount(new_price_base, 1.0))
            else:
                vals['amount'] = 0

            # Realizamos o backup do valor do campo
            # em casos onde o imposto deve respeitar um valor minimo
            vals['amount_original'] = vals['amount']

            # vals = self._check_tax_minimal_value(
            #     tax=tax, vals=vals, ignore_amount=ignore_amount)

            vals['base'] = new_price_base
            taxes.append(vals)

        return taxes

    def _compute_ii(self, price_base, currency_id):
        ii_tax = self.filtered(lambda x: x.domain == 'ii')

        if not ii_tax:
            return []

        vals = self._tax_vals(ii_tax)
        vals['amount'] = currency_id.round(ii_tax._compute_amount(price_base, 1.0))
        vals['base'] = price_base

        return [vals]

    def _compute_issqn(self, price_base, currency_id):
        issqn_tax = self.filtered(lambda x: x.domain == 'issqn')

        if not issqn_tax:
            return []

        service_locale = self.env.context.get('service_locale', False)
        issqn_tax_locale = self.env.context.get('issqn_tax_locale', False)

        vals = self._tax_vals(issqn_tax)

        # O calculo do imposto depende se o serviço foi
        # prestado dentro ou fora do municipio
        if service_locale and issqn_tax_locale and issqn_tax_locale in ('0', service_locale):
            vals['amount'] = currency_id.round(issqn_tax._compute_amount(price_base, 1.0))
        else:
            vals['amount'] = 0

        vals['base'] = price_base

        return [vals]

    def _compute_retention(self, price_base, currency_id):
        """Calcula retenções. O metodo realiza o calculo dos impostos
        CSLL, IRRF e INSS.

        Args:
            price_base (float): preço base para calculos dos impostos

        Returns:
            list: Lista contendo os impostos com sua base de calculo e valor
        """
        retention_tax = self.filtered(lambda x: x.domain in ('csll', 'irrf', 'inss'))  # noqa

        if not retention_tax:
            return []

        taxes = []

        inss_food_voucher = currency_id.round(self.env.context.get('inss_food_voucher', 0))
        inss_transportation_voucher = currency_id.round(self.env.context.get('inss_transportation_voucher', 0))
        inss_tools_supplies = currency_id.round(self.env.context.get('inss_tools_supplies', 0))

        service_locale = self.env.context.get('service_locale', False)

        csll_tax_locale = self.env.context.get('csll_tax_locale', False)
        irrf_tax_locale = self.env.context.get('irrf_tax_locale', False)
        inss_tax_locale = self.env.context.get('inss_tax_locale', False)

        for tax in retention_tax:
            vals = self._tax_vals(tax)

            if tax.domain == 'csll':
                tax_locale = csll_tax_locale
                # ignore_amount = self.env.context.get('csll_ignore_amount', False)

            if tax.domain == 'irrf':
                tax_locale = irrf_tax_locale
                # ignore_amount = self.env.context.get('irrf_ignore_amount', False)

            if tax.domain == 'inss':
                tax_locale = inss_tax_locale

                # No caso do inss, ha custos que devemos deduzir da base
                # de calculo do imposto, sendo os custos de vale-alimentacao
                # vale-transportes e outros custos como o de equipamento.
                # Caso o valor final seja negativo, o preco base fica zerado
                price_base_inss = max(0, price_base - inss_food_voucher - inss_transportation_voucher - inss_tools_supplies)  # noqa

                # O calculo do imposto depende se o serviço foi
                # prestado dentro ou fora do municipio
                if service_locale and tax_locale and tax_locale in ('0', service_locale):
                    vals['amount'] = currency_id.round(tax._compute_amount(price_base_inss, 1.0))
                else:
                    vals['amount'] = 0
            else:

                # O calculo do imposto depende se o serviço foi
                # prestado dentro ou fora do municipio
                if service_locale and tax_locale and tax_locale in ('0', service_locale):
                    vals['amount'] = currency_id.round(tax._compute_amount(price_base, 1.0))
                else:
                    vals['amount'] = 0

                # Realizamos o backup do valor do campo
                # em casos onde o imposto deve respeitar um valor minimo
                vals['amount_original'] = vals['amount']

                # vals = self._check_tax_minimal_value(tax=tax, vals=vals, ignore_amount=ignore_amount)

            vals['base'] = price_base

            taxes.append(vals)

        return taxes

    @api.multi
    def compute_all(self, price_unit, currency=None, quantity=1.0,
                    product=None, partner=None):

        exists_br_tax = len(self.filtered(lambda x: x.domain)) > 0

        if not exists_br_tax:
            res = super(AccountTax, self).compute_all(price_unit, currency, quantity, product, partner)  # noqa
            res['price_without_tax'] = round(price_unit * quantity, 2)
            return res

        if not currency:
            company_id = self.env.user.company_id if len(self) == 0 else self[0].company_id
            currency = company_id.currency_id

        price_base = price_unit * quantity

        ipi = self._compute_ipi(price_base, currency_id=currency)
        icms = self._compute_icms(price_base,
                                  ipi[0]['amount'] if ipi else 0.0,
                                  currency_id=currency)

        icmsst = self._compute_icms_st(price_base,
                                       ipi[0]['amount'] if ipi else 0.0,
                                       icms[0]['amount'] if icms else 0.0,
                                       currency_id=currency)

        difal = self._compute_difal(price_base,
                                    ipi[0]['amount'] if ipi else 0.0,
                                    currency_id=currency)

        taxes = icms + icmsst + difal + ipi

        taxes += self._compute_simples(price_base,
                                       currency_id=currency)

        taxes += self._compute_pis_cofins(price_base,
                                          icms[0]['amount'] if icms else 0.0,
                                          currency_id=currency)

        taxes += self._compute_issqn(price_base, currency_id=currency)
        taxes += self._compute_ii(price_base, currency_id=currency)
        taxes += self._compute_retention(price_base, currency_id=currency)

        total_included = total_excluded = financial_total_included = price_base  # noqa

        for tax in taxes:
            tax_id = self.filtered(lambda x: x.id == tax['id'])

            # Se o imposto esta marcado para ser somado
            # ao total
            if not tax_id.price_include:
                total_included += tax['amount']
                financial_total_included += tax['amount']

            # Se o imposto esta marcado para ser
            # somando ao total financeiro - usado
            # quando o total da nota difere do total financeiro
            if tax_id.price_include and tax_id.include_parcel_total:
                financial_total_included += tax['amount']

        return {
            'taxes': sorted(taxes, key=lambda k: k['sequence']),
            'total_excluded': total_excluded,
            'total_included': total_included,
            'financial_total_included': financial_total_included,
            'base': price_base,
        }
