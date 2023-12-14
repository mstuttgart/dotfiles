# © 2016 Danimar Ribeiro <danimaribeiro@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import copy
import re
import locale
import pytz

from datetime import datetime
from functools import reduce

import dateutil.relativedelta as relativedelta

from odoo import api, fields, models, tools
from odoo.exceptions import UserError

STATE = {'edit': [('readonly', False)]}


class InvoiceElectronic(models.Model):
    _name = 'invoice.electronic'

    _inherit = ['mail.thread']

    code = fields.Char(string='Código',
                       size=100,
                       required=True,
                       readonly=True,
                       states=STATE)

    name = fields.Char(string='Nome',
                       size=100,
                       required=True,
                       readonly=True,
                       states=STATE)

    company_id = fields.Many2one('res.company',
                                 string='Empresa',
                                 readonly=True,
                                 states=STATE)

    company_fiscal_type = fields.Selection(related='company_id.fiscal_type')

    state = fields.Selection([('draft', 'Provisório'),
                              ('edit', 'Editar'),
                              ('error', 'Erro'),
                              ('done', 'Enviado'),
                              ('cancel', 'Cancelado')],
                             string='State',
                             default='draft',
                             readonly=True,
                             states=STATE)

    tipo_operacao = fields.Selection([('entrada', 'Entrada'),
                                      ('saida', 'Saída')],
                                     string='Tipo de Operação',
                                     readonly=True,
                                     states=STATE)

    model = fields.Selection([('55', '55 - NFe'),
                              ('65', '65 - NFCe'),
                              ('001', 'NFS-e')],
                             string='Modelo',
                             readonly=True,
                             states=STATE)

    serie = fields.Many2one('br_account.document.serie',
                            string='Série',
                            readonly=True,
                            states=STATE)

    numero_prefixo = fields.Integer(string='Prefixo Número',
                                    readonly=True,
                                    states=STATE)

    numero = fields.Integer(string='Número',
                            readonly=True,
                            states=STATE)

    numero_controle = fields.Integer(string='Número de Controle',
                                     readonly=True,
                                     states=STATE)

    data_emissao = fields.Datetime(string='Data Emissão',
                                   readonly=True,
                                   states=STATE)

    data_fatura = fields.Datetime(string='Data Entrada/Saída',
                                  readonly=True,
                                  states=STATE)

    data_autorizacao = fields.Char(string='Data de Autorização',
                                   size=30,
                                   readonly=True,
                                   states=STATE)

    cancel_date = fields.Date(string='Data da Cancelamento',
                              readonly=True,
                              states=STATE)

    ambiente = fields.Selection([('homologacao', 'Homologação'),
                                 ('producao', 'Produção')],
                                string='Ambiente',
                                readonly=True,
                                states=STATE)

    invoice_id = fields.Many2one('account.invoice',
                                 string='Fatura',
                                 readonly=True,
                                 states=STATE,
                                 ondelete='cascade',
                                 index=True)

    partner_id = fields.Many2one('res.partner',
                                 string='Parceiro',
                                 readonly=True,
                                 states=STATE)

    commercial_partner_id = fields.Many2one('res.partner',
                                            string='Commercial Entity',
                                            related='',
                                            readonly=True,
                                            states=STATE)

    partner_shipping_id = fields.Many2one('res.partner',
                                          string='Entrega',
                                          readonly=True,
                                          states=STATE)

    payment_term_id = fields.Many2one('account.payment.term',
                                      string='Forma pagamento',
                                      ondelete='restrict',
                                      readonly=True,
                                      states=STATE)

    fiscal_position_id = fields.Many2one('account.fiscal.position',
                                         string='Posição Fiscal',
                                         readonly=True,
                                         ondelete='restrict',
                                         states=STATE)

    electronic_item_ids = fields.One2many('invoice.electronic.item',
                                          'invoice_electronic_id',
                                          string="Linhas",
                                          readonly=True,
                                          states=STATE)

    electronic_event_ids = fields.One2many('invoice.electronic.event',
                                           'invoice_electronic_id',
                                           string="Eventos",
                                           readonly=True,
                                           states=STATE)

    valor_bruto = fields.Monetary(string='Total Produtos',
                                  readonly=True,
                                  states=STATE)

    valor_desconto = fields.Monetary(string='Total Desconto',
                                     readonly=True,
                                     states=STATE)

    valor_bc_icms = fields.Monetary(string="Base de Cálculo ICMS",
                                    readonly=True,
                                    states=STATE)

    valor_icms = fields.Monetary(string="Total do ICMS",
                                 readonly=True,
                                 states=STATE)

    valor_icms_credito = fields.Monetary(string="Total do ICMS Crédito",
                                         readonly=True,
                                         states=STATE)

    valor_icms_deson = fields.Monetary(string='ICMS Desoneração',
                                       readonly=True,
                                       states=STATE)

    valor_bc_icmsst = fields.Monetary(string='Total Base ST',
                                      help="Total da base de cálculo do ICMS ST",
                                      readonly=True,
                                      states=STATE)

    valor_icmsst = fields.Monetary(string='Total ST',
                                   readonly=True,
                                   states=STATE)

    valor_ii = fields.Monetary(string='Total II',
                               readonly=True,
                               states=STATE)

    valor_ipi = fields.Monetary(string="Total IPI",
                                readonly=True,
                                states=STATE)

    valor_pis = fields.Monetary(string="Total PIS",
                                readonly=True,
                                states=STATE)

    valor_cofins = fields.Monetary(string="Total COFINS",
                                   readonly=True,
                                   states=STATE)

    valor_estimado_tributos = fields.Monetary(string="Tributos Estimados",
                                              readonly=True,
                                              states=STATE)

    valor_servicos = fields.Monetary(string="Total Serviços",
                                     readonly=True,
                                     states=STATE)

    valor_bc_issqn = fields.Monetary(string="Base ISS",
                                     readonly=True,
                                     states=STATE)

    valor_issqn = fields.Monetary(string="Total ISS",
                                  readonly=True, states=STATE)

    valor_pis_servicos = fields.Monetary(string="Total PIS Serviços",
                                         readonly=True,
                                         states=STATE)

    valor_cofins_servicos = fields.Monetary(string="Total Cofins Serviço",
                                            readonly=True,
                                            states=STATE)

    valor_retencao_issqn = fields.Monetary(string="Retenção ISSQN",
                                           readonly=True,
                                           states=STATE)

    valor_retencao_pis = fields.Monetary(string="Retenção PIS",
                                         readonly=True,
                                         states=STATE)

    valor_retencao_cofins = fields.Monetary(string="Retenção COFINS",
                                            readonly=True,
                                            states=STATE)

    valor_bc_irrf = fields.Monetary(string="Base de Cálculo IRRF",
                                    readonly=True,
                                    states=STATE)

    valor_retencao_irrf = fields.Monetary(string="Retenção IRRF",
                                          readonly=True,
                                          states=STATE)

    valor_bc_csll = fields.Monetary(string="Base de Cálculo CSLL",
                                    readonly=True,
                                    states=STATE)

    valor_csll = fields.Monetary(string='Valor CSLL',
                                 readonly=True,
                                 states=STATE)

    valor_retencao_csll = fields.Monetary(string="Retenção CSLL",
                                          readonly=True,
                                          states=STATE)

    valor_bc_inss = fields.Monetary(string="Base de Cálculo INSS",
                                    readonly=True,
                                    states=STATE)

    inss_food_voucher = fields.Float(string='Vale-Alimentação',
                                     readonly=True,
                                     states=STATE)

    inss_transportation_voucher = fields.Float(string='Vale-Tranporte',
                                               readonly=True,
                                               states=STATE)

    inss_tools_supplies = fields.Float(string='Equipamentos/Materiais',
                                       readonly=True,
                                       states=STATE)

    inss_deduction_total = fields.Float(string='Total Deduções do INSS',
                                        readonly=True,
                                        states=STATE)

    valor_inss = fields.Monetary(string='Valor INSS',
                                 readonly=True,
                                 states=STATE)

    valor_retencao_inss = fields.Monetary(string="Retenção INSS",
                                          help="Retenção Previdência Social",
                                          readonly=True,
                                          states=STATE)

    currency_id = fields.Many2one('res.currency',
                                  related='company_id.currency_id',
                                  string="Company Currency")

    valor_final = fields.Monetary(string='Valor Final',
                                  readonly=True,
                                  states=STATE)

    informacoes_legais = fields.Text(string='Informações legais',
                                     readonly=True,
                                     states=STATE)

    informacoes_complementares = fields.Text(string='Informações complementares',
                                             readonly=True,
                                             states=STATE)

    codigo_retorno = fields.Char(string='Código Retorno',
                                 readonly=True,
                                 states=STATE)

    mensagem_retorno = fields.Char(string='Mensagem Retorno',
                                   readonly=True,
                                   states=STATE)

    numero_nfe = fields.Char(string="Numero Formatado NFe",
                             readonly=True,
                             states=STATE)

    xml_to_send = fields.Binary(string="Xml a Enviar",
                                readonly=True)

    xml_to_send_name = fields.Char(string="Nome xml a ser enviado",
                                   size=100,
                                   readonly=True)

    email_sent = fields.Boolean(string="Email de confirmação na fila de email",
                                default=False,
                                readonly=True,
                                states=STATE)

    cancel_email_sent = fields.Boolean(string="Email de cancelamento na fila de email",
                                       default=False,
                                       readonly=True,
                                       states=STATE)

    cert_expire_date = fields.Date(string='Expire Date',
                                   related='invoice_id.cert_expire_date',
                                   readonly=True)

    days_to_expire_cert = fields.Integer(string='Days to Expire Certificate',
                                         related='invoice_id.days_to_expire_cert',
                                         default=60)

    cert_state = fields.Selection(string='Expire Certificate',
                                  related='invoice_id.cert_state')

    service_locale = fields.Selection(string='Serviço Prestado',
                                      selection=[
                                          ('1', 'No Município'),
                                          ('2', 'Fora do Município'),
                                      ],
                                      default='1')

    service_locale_address_id = fields.Many2one('res.partner',
                                                string='Endereço de Prestação de Serviço')

    public_location = fields.Boolean(string='Public Location')

    financial_price_total = fields.Monetary(string='Valor Total (Financeiro)',
                                            default=0.00)

    client_order_ref = fields.Char(
        string='Customer Reference',
        size=15,
        readonly=True,
        states=STATE,
        oldname='pedido_compra',
    )

    recibo_nfe = fields.Char(
        string='Recibo NFe',
        size=50,
        readonly=True,
        states=STATE,
    )

    def _create_attachment(self, prefix, event, data, extension='xml'):

        # Ajusta data para a timezone do usuario
        tz = pytz.timezone(self.env.user.partner_id.tz) or pytz.utc
        dt = pytz.utc.localize(fields.Datetime.now(self)).astimezone(tz)

        file_name = f"{prefix}-{dt.strftime('%Y-%m-%dT%H:%M:%S-03:00')}.{extension}"

        if extension != 'pdf':
            data = data.encode()

        attachment = self.env['ir.attachment'].create({
            'name': file_name,
            'datas': base64.b64encode(data),
            'datas_fname': file_name,
            'description': '',
            'res_model': 'invoice.electronic',
            'res_id': event.id
        })

        return attachment

    @api.multi
    def _hook_validation(self):
        """
            Override this method to implement the validations specific
            for the city you need
            @returns list<string> errors
        """
        errors = []
        if not self.serie.fiscal_document_id:
            errors.append('Nota Fiscal - Tipo de documento fiscal')

        if not self.serie.internal_sequence_id:
            errors.append('Nota Fiscal - Número da nota fiscal, a série deve ter uma sequencia interna')  # noqa

        # Emitente
        if not self.company_id.nfe_a1_file:
            errors.append('Emitente - Certificado Digital')

        if not self.company_id.nfe_a1_password:
            errors.append('Emitente - Senha do Certificado Digital')

        if not self.company_id.partner_id.legal_name:
            errors.append('Emitente - Razão Social')

        if not self.company_id.partner_id.cnpj_cpf:
            errors.append('Emitente - CNPJ/CPF')

        if not self.company_id.partner_id.street:
            errors.append('Emitente / Endereço - Logradouro')

        if not self.company_id.partner_id.number:
            errors.append('Emitente / Endereço - Número')

        if not self.company_id.partner_id.zip or len(re.sub(r"\D", "", self.company_id.partner_id.zip)) != 8:  # noqa
            errors.append('Emitente / Endereço - CEP')

        if not self.company_id.partner_id.state_id:
            errors.append('Emitente / Endereço - Estado')
        else:
            if not self.company_id.partner_id.state_id.ibge_code:
                errors.append('Emitente / Endereço - Cód. do IBGE do estado')

            if not self.company_id.partner_id.state_id.name:
                errors.append('Emitente / Endereço - Nome do estado')

        if not self.company_id.partner_id.city_id:
            errors.append('Emitente / Endereço - município')

        else:
            if not self.company_id.partner_id.city_id.name:
                errors.append('Emitente / Endereço - Nome do município')

            if not self.company_id.partner_id.city_id.ibge_code:
                errors.append('Emitente/Endereço - Cód. do IBGE do município')

        if not self.company_id.partner_id.country_id:
            errors.append('Emitente / Endereço - país')

        else:
            if not self.company_id.partner_id.country_id.name:
                errors.append('Emitente / Endereço - Nome do país')

            if not self.company_id.partner_id.country_id.bc_code:
                errors.append('Emitente / Endereço - Código do BC do país')

        partner = self.partner_id.commercial_partner_id
        company = self.company_id

        # Destinatário
        if partner.is_company and not partner.legal_name:
            errors.append('Destinatário - Razão Social')

        if partner.country_id.id == company.partner_id.country_id.id:
            if not partner.cnpj_cpf:
                errors.append('Destinatário - CNPJ/CPF')

        if not partner.street:
            errors.append('Destinatário / Endereço - Logradouro')

        if not partner.number:
            errors.append('Destinatário / Endereço - Número')

        if partner.country_id.id == company.partner_id.country_id.id:
            if not partner.zip or len(re.sub(r"\D", "", partner.zip)) != 8:  # noqa
                errors.append('Destinatário / Endereço - CEP')

        if partner.country_id.id == company.partner_id.country_id.id:

            if not partner.state_id:
                errors.append('Destinatário / Endereço - Estado')
            else:
                if not partner.state_id.ibge_code:
                    errors.append('Destinatário / Endereço - Código do IBGE \
                                  do estado')
                if not partner.state_id.name:
                    errors.append('Destinatário / Endereço - Nome do estado')

        if partner.country_id.id == company.partner_id.country_id.id:

            if not partner.city_id:
                errors.append('Destinatário / Endereço - Município')
            else:
                if not partner.city_id.name:
                    errors.append('Destinatário / Endereço - Nome do \
                                  município')
                if not partner.city_id.ibge_code:
                    errors.append('Destinatário / Endereço - Código do IBGE \
                                  do município')

        if not partner.country_id:
            errors.append('Destinatário / Endereço - País')

        else:
            if not partner.country_id.name:
                errors.append('Destinatário / Endereço - Nome do país')

            if not partner.country_id.bc_code:
                errors.append('Destinatário / Endereço - Cód. do BC do país')

        if self.service_locale == '2' and not self.service_locale_address_id:
            errors.append('Endereço de Prestação de Serviço')

        if self.service_locale_address_id:

            service_address = self.service_locale_address_id

            if not service_address.zip:
                errors.append('Endereço de Prestação de Serviço - CEP')

            if not service_address.street:
                errors.append('Endereço de Prestação de Serviço - Rua')

            if not service_address.number:
                errors.append('Endereço de Prestação de Serviço - Número')

            if not service_address.district:
                errors.append('Endereço de Prestação de Serviço - Bairro')

            if not service_address.city_id:
                errors.append('Endereço de Prestação de Serviço - Município')

            else:
                if not service_address.city_id.name:
                    errors.append('Endereço de Prestação de Serviço - Nome da Município')  # noqa

            if not service_address.state_id:
                errors.append('Endereço de Prestação de Serviço - Estado')
            else:
                if not service_address.state_id.code:
                    errors.append('Endereço de Prestação de Serviço - Código do IBGE do Estado ')  # noqa

            if not service_address.country_id:
                errors.append('Endereço de Prestação de Serviço - País')
            else:
                if not service_address.country_id.name:
                    errors.append(
                        'Endereço de Prestação de Serviço - Nome do País')

        # produtos
        for eletr in self.electronic_item_ids:

            if eletr.product_id:

                if not eletr.product_id.default_code:
                    errors.append('Prod: %s - Código do produto' % (eletr.product_id.name))  # noqa
        return errors

    def get_nfe_tribute_description(self):
        """Adicionamos os tributos Federal, Estadual e Municipal
           na descricao da NF em Informações Adicionais.

        Returns:
            str -- Texto com a descrição dos tributos da NFe
        """
        # Variavel Descrição a Retornar, default = ''
        description = ''

        # Verifica se a NF tem q destacar o total dos tributos
        # Segundo Lei NF de Serviço ou de Produto se For Venda
        # para Consumidor Final
        is_total_tributos = False
        fiscal_position_id = self.invoice_id.fiscal_position_id

        # Venda ou Serviço
        if fiscal_position_id.position_type in ('product', 'conjugate') and \
           fiscal_position_id.finalidade_emissao in ('1', '2') and \
           fiscal_position_id.ind_final == '1':
            is_total_tributos = True

        else:
            if fiscal_position_id.position_type == 'service':
                is_total_tributos = True

        # Descrição com o Total dos Tributos
        if is_total_tributos:
            lines = self.invoice_id.invoice_line_ids

            # Totaizando os Tributos
            total_federal = sum(lines.mapped('tributos_estimados_federais'))
            total_estadual = sum(lines.mapped('tributos_estimados_estaduais'))
            total_municipal = sum(lines.mapped(
                'tributos_estimados_municipais'))
            total_tributos = total_federal + total_estadual + total_municipal

            if total_tributos > 0:
                description = ('Val aprox. dos tributos: {} (Federal {}, Estadual {} e Municipal {}). Fonte: IBPT/empresometro.com.br')  # noqa

                # Definimos o locale como monetary de modo a formatar os valores
                # monetarios com o simbolo de R$ e virgula como separador decimal
                locale.setlocale(locale.LC_MONETARY, 'pt_BR.utf8')

                description = description.format(
                    locale.currency(total_tributos),
                    locale.currency(total_federal),
                    locale.currency(total_estadual),
                    locale.currency(total_municipal))

        # Adiciona Descrição dos Outros Impostos
        tax_description = '\n'

        # Adiciona Valor do Credito de ICMS
        # Obs.: Somente para Empresas do Simples
        if self.valor_bruto and self.valor_icms_credito and self.company_fiscal_type in ('1', '2'):
            # Calculando a Aliquota de Acordo com o Total dos Produtos e ICMS de Credito
            aliq_icms_credito = (
                self.valor_icms_credito * 100) / self.valor_bruto

            # Adicionando nas Observações da NF
            tax_description += 'Permite o Aproveitamento do Crédito de ICMS no Valor de %s' % locale.currency(self.valor_icms_credito, grouping=True)  # noqa
            tax_description += ' Correspondente a Alíquota de %.02f' % aliq_icms_credito  # noqa
            tax_description += '% nos Termos do Artigo 23 da LC 123/06.\n'

        # Adiciona INSS
        if self.valor_inss:
            if self.inss_food_voucher:
                tax_description += 'Vale-Alimentação = %s\n' % locale.currency(self.inss_food_voucher, grouping=True)  # noqa

            if self.inss_transportation_voucher:
                tax_description += 'Vale-Transporte = %s\n' % locale.currency(self.inss_transportation_voucher, grouping=True)  # noqa

            if self.inss_tools_supplies:
                tax_description += 'Material/Equipamento = %s\n' % locale.currency(self.inss_tools_supplies, grouping=True)  # noqa

            if self.inss_deduction_total:
                tax_description += 'Total Retenção Social = %s\n' % locale.currency(self.valor_final - self.inss_deduction_total, grouping=True)  # noqa

        # Adiciona Valor ISSQN
        if self.valor_issqn:
            tax_description += 'ISS {}% - {}'.format(self.electronic_item_ids[0].issqn_aliquota, locale.currency(self.valor_issqn, grouping=True))  # noqa

        # Caso tenha Alguma Descrição dos Outros Impostos Adicionar na NF
        if tax_description != '\n':
            description += tax_description

        return description

    @api.multi
    def _compute_legal_information(self):
        """ Metodo para Montar as Informações da Nota Fiscal
        """
        fiscal_ids = self.invoice_id.fiscal_observation_ids.filtered(lambda x: x.tipo == 'fiscal')  # noqa
        obs_ids = self.invoice_id.fiscal_observation_ids.filtered(lambda x: x.tipo == 'observacao')  # noqa

        prod_obs_ids = self.env['br_account.fiscal.observation'].browse()

        for item in self.invoice_id.invoice_line_ids:
            prod_obs_ids |= item.product_id.fiscal_observation_ids

        fiscal_ids |= prod_obs_ids.filtered(lambda x: x.tipo == 'fiscal')
        obs_ids |= prod_obs_ids.filtered(lambda x: x.tipo == 'observacao')

        fiscal = self._compute_msg(fiscal_ids) + (self.invoice_id.fiscal_comment or '')  # noqa
        observacao = self._compute_msg(obs_ids) + (self.invoice_id.comment or '')  # noqa
        tributos = self.get_nfe_tribute_description()

        if observacao != '' and tributos != '' and tributos[0:1] != '\n':
            observacao += '\n'

        # Adiciona os Tributos na Obs Complementares da NF
        observacao += tributos

        # Adicionando o Nr do Pedido e o Pedido do Cliente
        msg_pedido = ''

        if self.invoice_id.origin:
            msg_pedido += 'Nr(s) do(s) Pedido(s): ' + self.invoice_id.origin

        client_order_ref = self.client_order_ref or self.invoice_id.client_order_ref

        if client_order_ref:

            if msg_pedido != '':
                msg_pedido += ' // '

            msg_pedido += 'Referência do Cliente: ' + client_order_ref

        if observacao != '' and msg_pedido != '':
            observacao += '\n'

        # Adiciona Nrs dos Pedidos e Referencia do Cliente
        observacao += msg_pedido

        # Removendo \n\n duplicados
        observacao = observacao.replace('\n\n', '\n')

        self.informacoes_legais = fiscal
        self.informacoes_complementares = observacao

    def _compute_msg(self, observation_ids):
        from jinja2.sandbox import SandboxedEnvironment

        mako_template_env = SandboxedEnvironment(
            block_start_string="<%",
            block_end_string="%>",
            variable_start_string="${",
            variable_end_string="}",
            comment_start_string="<%doc>",
            comment_end_string="</%doc>",
            line_statement_prefix="%",
            line_comment_prefix="##",
            trim_blocks=True,  # do not output newline after
            autoescape=True,  # XML/HTML automatic escaping
        )

        def cmp(a, b):
            """O comando cmp foi removido no Python3. Este e
            um workaround ate que uma melhor solucao seja encontrada.
            """
            # TODO:Encontrar um substituto para o metodo cmp
            return (a > b) - (a < b)

        mako_template_env.globals.update({
            'str': str,
            'datetime': datetime,
            'len': len,
            'abs': abs,
            'min': min,
            'max': max,
            'sum': sum,
            'filter': filter,
            'reduce': reduce,
            'map': map,
            'round': round,
            'cmp': cmp,
            # dateutil.relativedelta is an old-style class and cannot be
            # instanciated wihtin a jinja2 expression, so a lambda "proxy" is
            # is needed, apparently.
            'relativedelta': lambda *a, **kw: relativedelta.relativedelta(
                *a, **kw),
        })

        mako_safe_env = copy.copy(mako_template_env)
        mako_safe_env.autoescape = False

        result = ''

        for item in observation_ids:

            if item.document_id and item.document_id.code != self.model:
                continue

            template = mako_safe_env.from_string(tools.ustr(item.message))

            variables = {
                'user': self.env.user,
                'ctx': self._context,
                'invoice': self.invoice_id,
            }

            render_result = template.render(variables)
            result += render_result + '\n'

        return result

    @api.multi
    def validate_invoice(self):
        self.ensure_one()
        errors = self._hook_validation()

        if len(errors) > 0:
            msg = "\n".join(["Por favor corrija os erros antes de prosseguir"] + errors)  # noqa
            raise UserError(msg)

    @api.multi
    def action_post_validate(self):
        self._compute_legal_information()

    @api.multi
    def action_print_einvoice_report(self):
        action = {
            "type": "ir.actions.act_url",
            "url": '',
            "target": "_blank",
        }
        return action

    @api.multi
    def _prepare_electronic_invoice_item(self, item, invoice):
        return {}

    @api.multi
    def _prepare_electronic_invoice_values(self):
        return {}

    @api.multi
    def action_send_electronic_invoice(self):
        """Metodo base para envio da doc. eletronicos. Deve
        ser sobrescrito nos modulos especificos de cada tipo de
        NFe.

        Raises:
            UserError: Quando a doc. eletronico esta no status 'done'
        """
        pass

    @api.multi
    def action_cancel_document(self, context=None, justificativa=None):
        """Metodo base para cancelamento do documento eletrônico.
        Este metodo deve ser herdado em metodos filhos para adaptar o
        cancelamento para cada tipo de prefeitura e normalmente pode
        ser chamado atraves de uma wizard.

        Keyword Arguments:
            context {dict} -- Dict contendo o 'context' do Odoo (default: {None})
            justificativa {str} -- Justificativa para o cancelamento do documento. (default: {None})
        """
        # Não pode Cancelar Edoc se tiver titulo pago
        if any(move for move in self.invoice_id.move_ids if move.paid_status in ['paid', 'partial']):
            raise UserError(
                'Você não pode cancelar uma fatura que foi paga ou parcialmente paga.'
                'Você precisa primeiro estornar os pagamentos relacionados a fatura.')

        values = {}

        if not self.cancel_date:
            values['cancel_date'] = fields.Date.today()

        # Se o doc. eletronico estiver nos estados
        # 'Provisorio' ou 'Editar' o cancelamento da
        # fatura irá automaticamente cancelar o doc. eletronico
        if self.state in ('draft', 'edit'):
            values['state'] = 'cancel'

        return self.write(values)

    @api.multi
    def action_back_to_draft(self):
        self.state = 'draft'

    @api.multi
    def action_edit_edoc(self):
        self.state = 'edit'

    def can_unlink(self):
        if self.state not in ('error', 'edit', 'done', 'cancel'):
            return True
        else:
            return False

    @api.multi
    def unlink(self):
        for item in self:
            if not item.can_unlink():
                raise UserError(
                    'Documento Eletrônico enviado - Proibido excluir')
        return super(InvoiceElectronic, self).unlink()

    def log_exception(self, exc):
        self.codigo_retorno = '-1'
        self.mensagem_retorno = exc

    @api.multi
    def cron_send_nfe(self):
        """Metodo executado pelo cron de NFe. O metodo filtra
        os doc. eletrônicos elegíveis para envio. Caso o certificado
        esteja expirado ou a sua fatura nao esteja confirmada,
        o doc. eletronico não sera enviado.
        """
        inv_obj = self.env['invoice.electronic'].with_context({
            'lang': self.env.user.lang,
            'tz': self.env.user.tz,
        })

        nfes = inv_obj.search([('state', 'in', ['draft'])], limit=15)

        # Verificamos os records que possuem certificado nao expirado
        nfes = nfes.filtered(lambda r: r.cert_state != 'expired')

        # Chama o metodo de envio dos doc. eletronico. Cada
        # tipo de Doc. eletronico tem seu proprio metodo de envio
        nfes.action_send_electronic_invoice()
