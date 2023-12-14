# © 2016 Danimar Ribeiro <danimaribeiro@gmail.com>, Trustcode
# © 2023 Michell Stuttgart <michell.faria@multidados.tech>, MultidadosTI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models
from odoo.addons import decimal_precision as dp
from odoo.addons.br_account.models.cst import CSOSN_SIMPLES, CST_ICMS, CST_IPI, CST_PIS_COFINS, ORIGEM_PROD

STATE = {'edit': [('readonly', False)]}


class InvoiceElectronicItem(models.Model):
    _name = 'invoice.electronic.item'
    _description = 'Invoice Electronic Item'

    name = fields.Text(
        string='Nome',
        readonly=True,
        states=STATE,
    )

    company_id = fields.Many2one(
        'res.company',
        string='Empresa',
        index=False,
        related='invoice_electronic_id.company_id',
        related_sudo=True,
        store=True
    )

    invoice_electronic_id = fields.Many2one(
        'invoice.electronic',
        string='Documento',
        readonly=True,
        ondelete='cascade',
        index=True
    )

    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id',
                                  string="Company Currency")

    state = fields.Selection(related='invoice_electronic_id.state',
                             string="State")

    product_id = fields.Many2one('product.product',
                                 string='Produto',
                                 readonly=True,
                                 states=STATE)

    tipo_produto = fields.Selection([('product', 'Produto'),
                                     ('service', 'Serviço')],
                                    string="Tipo Produto",
                                    readonly=True,
                                    states=STATE)

    cfop = fields.Char('CFOP', size=5, readonly=True, states=STATE)
    ncm = fields.Char('NCM', size=10, readonly=True, states=STATE)

    uom_id = fields.Many2one('uom.uom',
                             string='Unidade Medida',
                             readonly=True,
                             states=STATE)

    quantidade = fields.Float(string='Quantidade',
                              readonly=True,
                              states=STATE)

    preco_unitario = fields.Float(string='Preço Unitário',
                                  readonly=True,
                                  digits=dp.get_precision('Product Price'),
                                  states=STATE)

    desconto = fields.Float(string='Desconto',
                            readonly=True,
                            states=STATE)

    tributos_estimados = fields.Monetary(string='Valor Estimado Tributos',
                                         digits=dp.get_precision('Account'),
                                         readonly=True,
                                         states=STATE)

    valor_bruto = fields.Monetary(string='Valor Bruto',
                                  digits=dp.get_precision('Account'),
                                  readonly=True,
                                  states=STATE)

    valor_liquido = fields.Monetary(string='Valor Líquido',
                                    digits=dp.get_precision('Account'),
                                    readonly=True,
                                    states=STATE)

    indicador_total = fields.Selection([('0', '0 - Não'),
                                        ('1', '1 - Sim')],
                                       string="Compõe Total da Nota?",
                                       default='1',
                                       readonly=True,
                                       states=STATE)

    origem = fields.Selection(ORIGEM_PROD,
                              string='Origem Mercadoria',
                              readonly=True,
                              states=STATE)

    icms_cst = fields.Selection(CST_ICMS + CSOSN_SIMPLES,
                                string='Situação Tributária',
                                readonly=True,
                                states=STATE)

    icms_aliquota = fields.Float(string='Alíquota (ICMS)',
                                 digits=dp.get_precision('Account'),
                                 readonly=True,
                                 states=STATE)

    icms_tipo_base = fields.Selection([('0', '0 - Margem Valor Agregado (%)'),
                                       ('1', '1 - Pauta (Valor)'),
                                       ('2', '2 - Preço Tabelado Máx. (valor)'),
                                       ('3', '3 - Valor da operação')],
                                      string='Modalidade BC do ICMS',
                                      readonly=True,
                                      states=STATE)

    icms_base_calculo = fields.Monetary(string='Base de cálculo (ICMS)',
                                        digits=dp.get_precision('Account'),
                                        readonly=True,
                                        states=STATE)

    icms_aliquota_reducao_base = fields.Float(string='% Redução Base (ICMS)',
                                              digits=dp.get_precision(
                                                  'Account'),
                                              readonly=True,
                                              states=STATE)

    icms_valor = fields.Monetary(string='Valor Total (ICMS)',
                                 digits=dp.get_precision('Account'),
                                 readonly=True,
                                 states=STATE)

    icms_valor_credito = fields.Monetary(string="Valor de Cŕedito (ICMS)",
                                         digits=dp.get_precision('Account'),
                                         readonly=True,
                                         states=STATE)

    icms_aliquota_credito = fields.Float(string='% de Crédito (ICMS)',
                                         digits=dp.get_precision('Account'),
                                         readonly=True,
                                         states=STATE)

    icms_st_tipo_base = fields.Selection([('0', '0- Preço tabelado ou máximo  sugerido'),
                                          ('1', '1 - Lista Negativa (valor)'),
                                          ('2', '2 - Lista Positiva (valor)'),
                                          ('3', '3 - Lista Neutra (valor)'),
                                          ('4', '4 - Margem Valor Agregado (%)'),
                                          ('5', '5 - Pauta (valor)')],
                                         string='Tipo Base ICMS ST',
                                         required=True,
                                         default='4',
                                         readonly=True,
                                         states=STATE)

    icms_st_aliquota_mva = fields.Float(string='% MVA',
                                        digits=dp.get_precision('Account'),
                                        readonly=True,
                                        states=STATE)

    icms_st_aliquota = fields.Float(string='Alíquota (ICMSST)',
                                    digits=dp.get_precision('Account'),
                                    readonly=True,
                                    states=STATE)

    icms_st_base_calculo = fields.Monetary(string='Base de cálculo (ICMSST)',
                                           digits=dp.get_precision('Account'),
                                           readonly=True,
                                           states=STATE)

    icms_st_aliquota_reducao_base = fields.Float(string='% Redução Base (ICMSST)',
                                                 digits=dp.get_precision(
                                                     'Account'),
                                                 readonly=True,
                                                 states=STATE)

    icms_st_valor = fields.Monetary(string='Valor Total (ICMSST)',
                                    digits=dp.get_precision('Account'),
                                    readonly=True,
                                    states=STATE)

    icms_aliquota_diferimento = fields.Float(string='% Diferimento',
                                             digits=dp.get_precision(
                                                 'Account'),
                                             readonly=True,
                                             states=STATE)

    icms_valor_diferido = fields.Monetary(string='Valor Diferido',
                                          digits=dp.get_precision('Account'),
                                          readonly=True,
                                          states=STATE)

    icms_motivo_desoneracao = fields.Char(string='Motivo Desoneração',
                                          size=2,
                                          readonly=True,
                                          states=STATE)

    icms_valor_desonerado = fields.Monetary(string='Valor Desonerado',
                                            digits=dp.get_precision('Account'),
                                            readonly=True,
                                            states=STATE)

    # ----------- IPI -------------------

    ipi_cst = fields.Selection(CST_IPI, string='Situação tributária')

    ipi_aliquota = fields.Float(string='Alíquota (IPI)',
                                digits=dp.get_precision('Account'),
                                readonly=True,
                                states=STATE)

    ipi_base_calculo = fields.Monetary(string='Base de cálculo (IPI)',
                                       digits=dp.get_precision('Account'),
                                       readonly=True,
                                       states=STATE)

    ipi_reducao_bc = fields.Float(string='% Redução Base (IPI)',
                                  digits=dp.get_precision('Account'),
                                  readonly=True,
                                  states=STATE)

    ipi_valor = fields.Monetary(string='Valor Total (IPI)',
                                digits=dp.get_precision('Account'),
                                readonly=True,
                                states=STATE)

    # ----------- II ----------------------

    ii_base_calculo = fields.Monetary(string='Base de Cálculo',
                                      digits=dp.get_precision('Account'),
                                      readonly=True,
                                      states=STATE)

    ii_aliquota = fields.Float(string='Alíquota II',
                               digits=dp.get_precision('Account'),
                               readonly=True,
                               states=STATE)

    ii_valor_despesas = fields.Monetary(string='Despesas Aduaneiras',
                                        digits=dp.get_precision('Account'),
                                        readonly=True,
                                        states=STATE)

    ii_valor = fields.Monetary(string='Imposto de Importação',
                               digits=dp.get_precision('Account'),
                               readonly=True,
                               states=STATE)

    ii_valor_iof = fields.Monetary(string='IOF',
                                   digits=dp.get_precision('Account'),
                                   readonly=True,
                                   states=STATE)

    # ------------ PIS ---------------------

    pis_cst = fields.Selection(CST_PIS_COFINS,
                               string='PIS CST',
                               readonly=True,
                               states=STATE)

    pis_aliquota = fields.Float(string='Alíquota (PIS)',
                                digits=dp.get_precision('Account'),
                                readonly=True,
                                states=STATE)

    pis_base_calculo = fields.Monetary(string='Base de Cálculo (PIS)',
                                       digits=dp.get_precision('Account'),
                                       readonly=True,
                                       states=STATE)

    pis_valor = fields.Monetary(string='Valor Total do (PIS)',
                                digits=dp.get_precision('Account'),
                                readonly=True,
                                states=STATE)

    pis_valor_retencao = fields.Monetary(string='Valor Retido do (PIS)',
                                         digits=dp.get_precision('Account'),
                                         readonly=True,
                                         states=STATE)

    # ------------ COFINS ------------
    cofins_cst = fields.Selection(CST_PIS_COFINS,
                                  string='COFINS CST',
                                  readonly=True,
                                  states=STATE)

    cofins_aliquota = fields.Float(string='Alíquota (COFINS)',
                                   digits=dp.get_precision('Account'),
                                   readonly=True,
                                   states=STATE)

    cofins_base_calculo = fields.Monetary(string='Base de Cálculo (COFINS)',
                                          digits=dp.get_precision('Account'),
                                          readonly=True,
                                          states=STATE)

    cofins_valor = fields.Monetary(string='Valor Total (COFINS)',
                                   digits=dp.get_precision('Account'),
                                   readonly=True,
                                   states=STATE)

    cofins_valor_retencao = fields.Monetary(string='Valor Retido (COFINS)',
                                            digits=dp.get_precision('Account'),
                                            readonly=True,
                                            states=STATE)

    # ----------- ISSQN -------------

    issqn_codigo = fields.Char(string='Código',
                               size=10,
                               readonly=True,
                               states=STATE)

    issqn_aliquota = fields.Float(string='Alíquota (ISSQN)',
                                  digits=dp.get_precision('Account'),
                                  readonly=True,
                                  states=STATE)

    issqn_base_calculo = fields.Monetary(string='Base de Cálculo (ISSQN)',
                                         digits=dp.get_precision('Account'),
                                         readonly=True,
                                         states=STATE)

    issqn_valor = fields.Monetary(string='Valor Total (ISSQN)',
                                  digits=dp.get_precision('Account'),
                                  readonly=True,
                                  states=STATE)

    issqn_valor_retencao = fields.Monetary(string='Valor Retenção (ISSQN)',
                                           digits=dp.get_precision('Account'),
                                           readonly=True,
                                           states=STATE)

    # ------------ RETENÇÔES ------------
    csll_base_calculo = fields.Monetary(string='Base de Cálculo (CSLL)',
                                        digits=dp.get_precision('Account'),
                                        readonly=True,
                                        states=STATE)

    csll_aliquota = fields.Float(string='Alíquota (CSLL)',
                                 digits=dp.get_precision('Account'),
                                 readonly=True,
                                 states=STATE)

    csll_valor_retencao = fields.Monetary(string='Valor Retenção (CSLL)',
                                          digits=dp.get_precision('Account'),
                                          readonly=True,
                                          states=STATE)

    irrf_base_calculo = fields.Monetary(string='Base de Cálculo (IRRF)',
                                        digits=dp.get_precision('Account'),
                                        readonly=True,
                                        states=STATE)

    irrf_aliquota = fields.Float(string='Alíquota (IRRF)',
                                 digits=dp.get_precision('Account'),
                                 readonly=True,
                                 states=STATE)

    irrf_valor_retencao = fields.Monetary(string='Valor Retenção (IRRF)',
                                          digits=dp.get_precision('Account'),
                                          readonly=True,
                                          states=STATE)

    inss_base_calculo = fields.Monetary(string='Base de Cálculo (INSS)',
                                        digits=dp.get_precision('Account'),
                                        readonly=True,
                                        states=STATE)

    inss_food_voucher = fields.Float(string='Vale-Alimentação',
                                     digits=dp.get_precision('Account'),
                                     readonly=True,
                                     states=STATE)

    inss_transportation_voucher = fields.Float(string='Vale-Tranporte',
                                               digits=dp.get_precision('Account'),  # noqa
                                               readonly=True,
                                               states=STATE)

    inss_tools_supplies = fields.Float(string='Equipamentos/Materiais',
                                       digits=dp.get_precision('Account'),
                                       readonly=True,
                                       states=STATE)

    inss_aliquota = fields.Float(string='Alíquota (INSS)',
                                 digits=dp.get_precision('Account'),
                                 readonly=True,
                                 states=STATE)

    inss_valor_retencao = fields.Monetary(string='Valor Retenção (INSS)',
                                          digits=dp.get_precision('Account'),
                                          readonly=True,
                                          states=STATE)

    financial_price_total = fields.Monetary(string='Valor Líquido (Financeiro)',
                                            default=0.00)

    invoice_line_id = fields.Many2one('account.invoice.line',
                                      string='Linha da Fatura')

    client_order_ref = fields.Char(
        string='Customer Reference',
        size=15,
        oldname='pedido_compra',
        help="Se setado aqui sobrescreve o pedido de compra da fatura",
    )

    client_order_item_ref = fields.Char(
        string='Customer Reference Item',
        size=6,
        oldname='item_pedido_compra',
        help='Item do pedido de compra do cliente',
    )
