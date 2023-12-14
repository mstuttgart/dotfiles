# © 2016 Danimar Ribeiro <danimaribeiro@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import hashlib
import base64
import logging
import re
import pytz
import time
import qrcode
import urllib3
import requests

from io import BytesIO

from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT

from odoo.addons.br_nfe.models.const import (FINALIDADE_EMISSAO,
                                             IND_FINAL,
                                             IND_PRES,
                                             IND_INTERMED,
                                             IND_FINAL,
                                             IND_DEST,
                                             INDICADOR_IE_DEST,
                                             MODALIDADE_FRETE,
                                             FORMA_PAGAMENTO)

_logger = logging.getLogger(__name__)

try:
    from pytrustnfe.nfe import autorizar_nfe
    from pytrustnfe.nfe import xml_autorizar_nfe
    from pytrustnfe.nfe import retorno_autorizar_nfe
    from pytrustnfe.nfe import recepcao_evento_cancelamento
    from pytrustnfe.nfe import consultar_protocolo_nfe
    from pytrustnfe.certificado import Certificado
    from pytrustnfe.utils import ChaveNFe, gerar_chave, gerar_nfeproc, gerar_nfeproc_cancel
    from pytrustnfe.xml.validate import valida_nfe
    from pytrustnfe.nfe.danfe import danfe
    from pytrustnfe.urls import url_qrcode, url_qrcode_exibicao
except ImportError:
    _logger.info('Cannot import pytrustnfe', exc_info=True)

STATE = {'edit': [('readonly', False)]}


class InvoiceElectronic(models.Model):
    _inherit = 'invoice.electronic'

    state = fields.Selection(selection_add=[('denied', 'Denegado')])

    ambiente_nfe = fields.Selection(string='Ambiente NFe',
                                    related='company_id.tipo_ambiente',
                                    readonly=True)

    finalidade_emissao = fields.Selection(FINALIDADE_EMISSAO,
                                          string='Finalidade',
                                          default='1',
                                          help="Finalidade da emissão de NFe",)

    ind_final = fields.Selection(IND_FINAL,
                                 string='Consumidor Final',
                                 readonly=True,
                                 states=STATE,
                                 required=False,
                                 default='0',
                                 help='Indica operação com Consumidor final.')

    ind_pres = fields.Selection(IND_PRES,
                                string='Indicador de Presença',
                                readonly=True,
                                states=STATE,
                                required=False,
                                default='0',
                                help='Indicador de presença do comprador no\n'
                                     'estabelecimento comercial no momento\n'
                                     'da operação.')

    ind_intermed = fields.Selection(IND_INTERMED,
                                    string='Ind. de Intermediário',
                                    help="""Indicador de Intermediário/Marktplace.
                                    * Considera-se intermediador/marketplace os prestadores de serviços e de negócios referentes às transações comerciais ou de prestação de serviços intermediadas, realizadas por pessoas jurídicas ou pessoas físicas.
                                    * Considera-se site/plataforma própria as vendas que não foram intermediadas (por marketplace), como venda em site próprio, teleatendimento.""")

    cnpj_intermed = fields.Char(string='CNPJ do Intermediador',
                                help="""Informar o CNPJ do Intermediador da Transação (agenciador, plataforma de delivery, marketplace e similar) de serviços e de negócios.""")  # noqa

    id_cad_int_tran = fields.Char(string='Cadastrado no Intermediador',
                                  help="""Nome do usuário ou identificação do perfil do vendedor no site do intermediador (agenciador, plataforma de delivery, marketplace e similar) de serviços e de negócios.""")  # noqa

    ind_dest = fields.Selection(IND_DEST,
                                string='Indicador Destinatário',
                                readonly=True,
                                states=STATE)

    ind_ie_dest = fields.Selection(INDICADOR_IE_DEST,
                                   string='Indicador IE Dest.',
                                   help='Indicador da IE do destinatário',
                                   readonly=True,
                                   states=STATE)

    tipo_emissao = fields.Selection([('1', '1 - Emissão normal'),
                                     ('2', '2 - Contingência FS-IA, '
                                           'com impressão do DANFE em '
                                           'formulário de segurança'),
                                     ('3', '3 - Contingência SCAN'),
                                     ('4', '4 - Contingência DPEC'),
                                     ('5', '5 - Contingência FS-DA, com '
                                           'impressão do DANFE em formulário '
                                           'de segurança'),
                                     ('6', '6 - Contingência SVC-AN'),
                                     ('7', '7 - Contingência SVC-RS'),
                                     ('9', '9 - Contingência off-line da NFC-e')],  # noqa: 501
                                    string='Tipo de Emissão',
                                    readonly=True,
                                    states=STATE,
                                    default='1')

    # Transporte
    modalidade_frete = fields.Selection(MODALIDADE_FRETE,
                                        string='Modalidade do frete',
                                        default='9',
                                        readonly=True,
                                        states=STATE)

    valor_frete = fields.Monetary(string='Total Frete',
                                  readonly=True,
                                  states=STATE)

    valor_seguro = fields.Monetary(string='Total Seguro',
                                   readonly=True,
                                   states=STATE)

    valor_despesas = fields.Monetary(string='Total Despesas',
                                     readonly=True,
                                     states=STATE)

    transportadora_id = fields.Many2one('res.partner',
                                        string='Transportadora',
                                        readonly=True,
                                        states=STATE)

    placa_veiculo = fields.Char(string='Placa do Veículo',
                                size=7,
                                readonly=True,
                                states=STATE)

    uf_veiculo = fields.Char(string='UF da Placa',
                             size=2,
                             readonly=True,
                             states=STATE)

    rntc = fields.Char(string='RNTC',
                       size=20,
                       readonly=True,
                       states=STATE,
                       help='Registro Nacional de Transportador de Carga')

    reboque_ids = fields.One2many(comodel_name='nfe.reboque',
                                  inverse_name='invoice_electronic_id',
                                  string='Reboques',
                                  readonly=True,
                                  states=STATE)

    volume_ids = fields.One2many(comodel_name='nfe.volume',
                                 inverse_name='invoice_electronic_id',
                                 string='Volumes',
                                 readonly=True,
                                 states=STATE)

    # Exportação
    uf_saida_pais_id = fields.Many2one('res.country.state',
                                       domain=[('country_id.code', '=', 'BR')],
                                       string='UF Saída do País',
                                       readonly=True,
                                       states=STATE)

    local_embarque = fields.Char(string='Local de Embarque',
                                 size=60,
                                 readonly=True,
                                 states=STATE)

    local_despacho = fields.Char(string='Local de Despacho',
                                 size=60,
                                 readonly=True,
                                 states=STATE)

    # Cobrança
    numero_fatura = fields.Char(string='Número da Fatura',
                                readonly=True,
                                states=STATE)

    fatura_bruto = fields.Monetary(string='Valor Original',
                                   readonly=True,
                                   states=STATE)

    fatura_desconto = fields.Monetary(string='Desconto',
                                      readonly=True,
                                      states=STATE)

    fatura_liquido = fields.Monetary(string='Valor Líquido',
                                     readonly=True,
                                     states=STATE)

    duplicata_ids = fields.One2many(comodel_name='nfe.duplicata',
                                    inverse_name='invoice_electronic_id',
                                    string='Duplicatas',
                                    readonly=True,
                                    states=STATE)

    # Compras
    nota_empenho = fields.Char(string='Nota de Empenho',
                               size=22,
                               readonly=True,
                               states=STATE)

    pedido_compra = fields.Char(string='Pedido Compra',
                                size=60,
                                readonly=True,
                                states=STATE)

    contrato_compra = fields.Char(string='Contrato Compra',
                                  size=60,
                                  readonly=True,
                                  states=STATE)

    sequencial_evento = fields.Integer(string='Sequêncial Evento',
                                       default=1,
                                       readonly=True,
                                       states=STATE)

    chave_nfe = fields.Char(string='Chave NFe',
                            size=50,
                            readonly=True,
                            states=STATE)

    chave_nfe_danfe = fields.Char(string='Chave Formatado',
                                  compute='_format_danfe_key')

    protocolo_nfe = fields.Char(string='Protocolo',
                                size=50,
                                readonly=True,
                                states=STATE,
                                help='Protocolo de autorização da NFe')

    nfe_processada = fields.Binary(string='Xml da NFe', readonly=True)

    nfe_processada_name = fields.Char(string='Xml da NFe Nome',
                                      size=100,
                                      readonly=True)

    valor_icms_uf_remet = fields.Monetary(string='ICMS Remetente',
                                          readonly=True,
                                          states=STATE,
                                          help='Valor total do ICMS '
                                               'Interestadual para a UF do '
                                               'Remetente')

    valor_icms_uf_dest = fields.Monetary(string='ICMS Destino',
                                         readonly=True,
                                         states=STATE,
                                         help='Valor total do ICMS '
                                              'Interestadual para a UF de '
                                              'destino')

    valor_icms_fcp_uf_dest = fields.Monetary(string='Total ICMS FCP',
                                             readonly=True,
                                             states=STATE,
                                             help='Total total do ICMS '
                                                  'relativo Fundo de Combate '
                                                  'à Pobreza (FCP) da UF de '
                                                  'destino')

    # Documentos Relacionados
    fiscal_document_related_ids = fields.One2many(comodel_name='br_account.document.related',  # noqa: 501
                                                  inverse_name='invoice_electronic_id',  # noqa: 501
                                                  string='Documentos Fiscais Relacionados',  # noqa: 501
                                                  readonly=True, states=STATE)

    # CARTA DE CORRECAO
    cartas_correcao_ids = fields.One2many(comodel_name='carta.correcao.eletronica.evento',  # noqa: 501
                                          inverse_name='electronic_doc_id',
                                          string='Cartas de Correção',
                                          readonly=True,
                                          states=STATE)

    natureza_operacao = fields.Char(string='Natureza da Operação')

    complementar_ids = fields.One2many('invoice.electronic',
                                       inverse_name='parent_edoc_id',
                                       string='Complementar')

    count_complementar_ids = fields.Integer(string="Total NFe",
                                            compute='_compute_count_complementar_ids')

    parent_edoc_id = fields.Many2one(
        'invoice.electronic', string='EDoc Gerador')

    # NFC-e
    qrcode_url = fields.Char(string='URL de Consulta')
    chave_url = fields.Char(string='URL da Chave')

    statement_ids = fields.Many2many('account.bank.statement.line',
                                     string='Pagamentos')

    @api.depends('complementar_ids')
    def _compute_count_complementar_ids(self):
        """Calcula quantidade de NFe Complementar relacionado
        ao doc. eletronico.
        """
        for rec in self:
            rec.count_complementar_ids = len(rec.complementar_ids.ids)

    @api.multi
    def action_view_complementar_edocs(self):

        if self.count_complementar_ids == 1:

            _, act_id = self.env['ir.model.data'].get_object_reference(
                'br_account_einvoice', 'action_sped_base_electronic_doc')

            _, view_id = self.env['ir.model.data'].get_object_reference(
                'br_account_einvoice', 'br_account_invoice_electronic_form')

            vals = self.env['ir.actions.act_window'].browse(act_id).read()[0]
            vals['view_id'] = (view_id, 'sped.electronic.doc.form')
            vals['views'][1] = (view_id, 'form')
            vals['views'] = [vals['views'][1], vals['views'][0]]

            vals['res_id'] = self.complementar_ids[0].id

            return vals

        else:
            _, act_id = self.env['ir.model.data'].get_object_reference(
                'br_account_einvoice', 'action_sped_base_electronic_doc')

            vals = self.env['ir.actions.act_window'].browse(act_id).read()[0]
            vals['domain'] = [('id', 'in', self.complementar_ids.ids)]

            return vals

    @api.multi
    @api.depends('chave_nfe')
    def _format_danfe_key(self):
        for item in self:
            item.chave_nfe_danfe = re.sub("(.{4})", "\\1.", item.chave_nfe or '', 10, re.DOTALL)  # noqa: 501

    @api.multi
    def generate_correction_letter(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.carta.correcao.eletronica',
            'views': [[False, 'form']],
            'name': 'Carta de Correção',
            'target': 'new',
            'context': {'default_electronic_doc_id': self.id},
        }

    def barcode_from_chave_nfe(self):
        """ Gera o codigo de barras a partir da chave da NFe. Utilizamos este
        metodo ao inves de utilizar request porque precisamos dele para envio
        do DANFE por email. Quando o DANFe e enviado pela fila de email o mesmo
        nao consegue chamar o metodo de geracao de codigo de barras do
        controller. Sendo precisamos gerar o DANFE diretamente.

        :return: Imagem do DANFE em Base64
        :rtype: str
        """

        try:
            barcode = self.env['ir.actions.report'].barcode('Code128',
                                                            self.chave_nfe,
                                                            width=600,
                                                            height=100,
                                                            humanreadable=0)
        except ValueError as exc:
            _logger.info('Cannot convert inn barcode. %s' % exc,
                         exc_info=True)
        return base64.b64encode(barcode).decode('utf-8')

    def can_unlink(self):
        res = super(InvoiceElectronic, self).can_unlink()
        return False if self.state == 'denied' else res

    @api.multi
    def unlink(self):
        for item in self:
            if item.state == 'denied':
                raise UserError(
                    'Documento Eletrônico Denegado - Proibido excluir')
        return super(InvoiceElectronic, self).unlink()

    @api.multi
    def _hook_validation(self):
        errors = super(InvoiceElectronic, self)._hook_validation()

        if self.model not in ('55', '65'):
            return errors

        # Verificamos se o modulo br_pos_base esta instalado
        br_pos_base_not_installed = self.env['ir.module.module'].sudo().search([
            ('name', '=', 'br_pos_base'), ('state', '!=', 'installed')])

        # Modulo de emissao de NFE dependen inderetamente do modulo de POS
        # O modulo br_nfe nao depende diretamente do POS por causa de outros tipos
        # de nfe que o modulo transmite.
        if self.model == '65' and br_pos_base_not_installed:
            errors.append(
                'Para emissão de NFCe, faz-se necessário que o modulo POS esteja instalado.')

        # Geral (NFe e NFCe)
        if not self.company_id.partner_id.inscr_est:
            errors.append('Emitente / Inscrição Estadual')

        if self.ind_ie_dest not in ('1', '2', '9'):
            errors.append('Indicador da IE do Destinatário inválido')

        if not self.fiscal_position_id:
            errors.append('Configure a posição fiscal')

        if self.company_id.accountant_id and not self.company_id.accountant_id.cnpj_cpf:  # noqa
            errors.append('Emitente / CNPJ do escritório contabilidade')

        fone = re.sub('[^0-9]', '', self.company_id.phone or '')

        if fone and len(fone) < 6 or len(fone) > 14:
            errors.append(
                'Telefone do emitente deve possuir entre 6 e 14 digitos')

        fone = re.sub('[^0-9]', '', self.commercial_partner_id.phone or '')

        if fone and len(fone) < 6 or len(fone) > 14:
            errors.append(
                'Telefone do destinatário deve possuir entre 6 e 14 digitos')

        # finalidade_emissao '4' é devolucao. Entao devemos ter os documentos
        # relacionados preenchidos
        if self.fiscal_position_id.finalidade_emissao == '4':

            if not self.fiscal_document_related_ids:
                errors.append(
                    'Preencher \'Documentos Relacionados\' com dados da fatura original')

            if self.invoice_id.journal_type != 'sale_no_financial':
                errors.append(
                    'NFe de Devolução deve ter um diário do tipo \'Venda (sem financeiro)\'')

        # finalidade_emissao '1.1' é Simples Remssa. Entao devemos ter o diario Simples Remessa
        # para que não seja gerado Financeiro
        elif self.fiscal_position_id.finalidade_emissao == '1.1':

            if self.invoice_id.journal_type != 'simples_remessa':
                errors.append(
                    'NFe de Simples Remessa deve ter um diário do tipo \'Simples Remessa\'')

        elif not self.payment_term_id.internal_use and self.payment_term_id.indPag not in ('0', '1'):

            # Indicador de pagamento para NFe de Venda aceita apenas valores '0' e '1'
            errors.append("Selecionar 'Pagamento à Vista' ou 'Pagamento à Prazo' no campo 'Indicador de Pagamento' da 'Condição de Pagamento' selecionada na fatura")  # noqa

        # Para NFe que não são de Simples Remessa, Complementar, Devolução ou Ajuste, devemos ter o Meio de Pagamento
        # selecionado na tarefa
        if self.fiscal_position_id.finalidade_emissao not in ('1.1', '3', '4') and self.finalidade_emissao != '2':

            if not all(parcel.title_type_id.nfe_tpag for parcel in self.invoice_id.parcel_ids):
                raise('O Tipo de Título utilizado nas parcelas não possui \'Meio de Pagamento\'. Por favor, atribua um Meio de Pagamento a ele.')  # noqa

        if self.fiscal_position_id.ind_pres in ('2', '3', '4', '9') and not self.fiscal_position_id.ind_intermed:
            errors.append(
                "Preencher campo 'Ind. de Intermediário' na Posição Fiscal")

        for eletr in self.electronic_item_ids:

            prod = "Produto: %s - %s" % (eletr.product_id.default_code,
                                         eletr.product_id.name)

            if not eletr.origem:
                errors.append('%s - Origem' % prod)

            if not eletr.cfop:
                errors.append('%s - CFOP' % prod)

            elif self.model == '55':

                # Para NFe de Saida, a CFOP deve começar com os digitos 5 (mesmo estado),
                # 6 (interestadual) ou 7 (exterior)
                if self.tipo_operacao == 'saida':

                    if (self.ind_dest == '1' and eletr.cfop[0] != '5') or (self.ind_dest == '2' and eletr.cfop[0] != '6') or (self.ind_dest == '3' and eletr.cfop[0] != '7'):
                        errors.append('%s - CFOP %s incompativel com a Indicador de Destinatário "%s"' % (prod, eletr.cfop, self.ind_dest))  # noqa

                # Para NFe de Entrada, a CFOP deve começar com os digitos 1 (mesmo estado),
                # 2 (interestadual) ou 3 (exterior)
                if self.tipo_operacao == 'entrada':

                    if (self.ind_dest == '1' and eletr.cfop[0] != '1') or (self.ind_dest == '2' and eletr.cfop[0] != '2') or (self.ind_dest == '3' and eletr.cfop[0] != '3'):
                        errors.append('%s - CFOP %s incompativel com a Indicador de Destinatário "%s"' % (prod, eletr.cfop, self.ind_dest))  # noqa

            if eletr.tipo_produto == 'product':

                if not eletr.icms_cst:
                    errors.append('%s - CST do ICMS' % prod)

                if not eletr.ipi_cst:
                    errors.append('%s - CST do IPI' % prod)

            if eletr.tipo_produto == 'service':

                if not eletr.issqn_codigo:
                    errors.append('%s - Código de Serviço' % prod)

                if not self.company_id.inscr_mun:
                    errors.append('Emitente / Inscrição Municipal')

            if not eletr.pis_cst:
                errors.append('%s - CST do PIS' % prod)

            if not eletr.cofins_cst:
                errors.append('%s - CST do Cofins' % prod)

        # Especifico para NFC-e
        if self.model == '65':

            if not self.company_id.id_token_csc:
                errors.append('Identificador do CSC inválido')

            if not len(self.company_id.csc or ''):
                errors.append('CSC Inválido')

            if len(self.serie) == 0:
                errors.append('Número de Série da NFe Inválido')

        return errors

    @api.multi
    def _prepare_electronic_invoice_item(self, item, invoice):
        res = super(InvoiceElectronic, self)._prepare_electronic_invoice_item(item, invoice)  # noqa: 501

        if self.model not in ('55', '65'):
            return res

        partner = item.invoice_electronic_id.partner_id
        fiscal_position = item.invoice_electronic_id.fiscal_position_id

        company = item.invoice_electronic_id.company_id
        barcode_cean = item.product_id.barcode or 'SEM GTIN' if company.barcode_in_nf_xml else 'SEM GTIN'  # noqa

        precision = self.env['decimal.precision'].precision_get(
            'Product Price')
        format_unit = '%.{precision}f'.format(precision=precision)

        if self.ambiente == 'homologacao':
            x_prod = 'NOTA FISCAL EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL'
        else:
            x_prod = item.product_description[:120]  # limite do tamanho do campo para NFe

        prod = {
            'cProd': item.product_id.default_code,
            'cEAN': barcode_cean,
            'xProd': x_prod,
            'NCM': re.sub('[^0-9]', '', item.ncm or '')[:8] if item.tipo_produto == 'product' else '00',
            'EXTIPI': re.sub('[^0-9]', '', item.ncm or '')[8:],
            'CFOP': item.cfop,
            'uCom': '{:.6}'.format(item.uom_id.name or ''),
            'qCom': item.quantidade,
            'vUnCom': format_unit % item.preco_unitario,
            'vProd': "%.02f" % item.valor_bruto,
            'cEANTrib': barcode_cean,
            'uTrib': '{:.6}'.format(item.uom_id.name or ''),
            'qTrib': item.quantidade,
            'vUnTrib': format_unit % item.preco_unitario,
            'vFrete': "%.02f" % item.frete if item.frete else '',
            'vSeg': "%.02f" % item.seguro if item.seguro else '',
            'vDesc': "%.02f" % item.desconto if item.desconto else '',
            'vOutro': "%.02f" % item.outras_despesas if item.outras_despesas else '',  # noqa
            'indTot': item.indicador_total,
            'cfop': item.cfop,
            'CEST': re.sub('[^0-9]', '', item.cest or ''),
        }

        # O Numero do Pedido de Compra do item tem prioridade sobre o do edoc
        prod.update({
            'xPed': item.client_order_ref or item.invoice_electronic_id.client_order_ref or '',  # noqa
            'nItemPed': item.client_order_item_ref or '',
        })

        impostoDevol = {}
        di_vals = []

        for di in item.import_declaration_ids:
            adicoes = []

            for adi in di.line_ids:
                adicoes.append({
                    'nAdicao': adi.name,
                    'nSeqAdic': adi.sequence,
                    'cFabricante': adi.manufacturer_code,
                    'vDescDI': "%.02f" % adi.amount_discount
                    if adi.amount_discount else '',
                    'nDraw': adi.drawback_number or '',
                })

            dt_registration = datetime.strptime(
                di.date_registration, DATE_FORMAT)

            dt_release = datetime.strptime(di.date_release, DATE_FORMAT)

            di_vals.append({
                'nDI': di.name,
                'dDI': dt_registration.strftime('%Y-%m-%d'),
                'xLocDesemb': di.location,
                'UFDesemb': di.state_id.code,
                'dDesemb': dt_release.strftime('%Y-%m-%d'),
                'tpViaTransp': di.type_transportation,
                'vAFRMM': "%.02f" % di.afrmm_value if di.afrmm_value else '',
                'tpIntermedio': di.type_import,
                'CNPJ': di.thirdparty_cnpj or '',
                'UFTerceiro': di.thirdparty_state_id.code or '',
                'cExportador': di.exporting_code,
                'adi': adicoes,
            })

        prod["DI"] = di_vals

        # Aqui montamos a tag de imposto da NFe
        imposto = {
            'vTotTrib': "%.02f" % item.tributos_estimados,
        }

        if item.tipo_produto == 'product':
            imposto['ICMS'] = {
                'orig': item.origem,
                'CST': item.icms_cst,
                'modBC': item.icms_tipo_base,
                'vBC': "%.02f" % item.icms_base_calculo,
                'pRedBC': "%.02f" % item.icms_aliquota_reducao_base,
                'pICMS': "%.02f" % item.icms_aliquota,
                'vICMS': "%.02f" % item.icms_valor,
                'modBCST': item.icms_st_tipo_base,
                'pMVAST': "%.02f" % item.icms_st_aliquota_mva,
                'pRedBCST': "%.02f" % item.icms_st_aliquota_reducao_base,
                'vBCST': "%.02f" % item.icms_st_base_calculo,
                'pICMSST': "%.02f" % item.icms_st_aliquota,
                'vICMSST': "%.02f" % item.icms_st_valor,
                'pCredSN': "%.02f" % item.icms_aliquota_credito,
                'vCredICMSSN': "%.02f" % item.icms_valor_credito,
            }

            if item.icms_cst in ('60', '500') and item.invoice_electronic_id.ind_final == '0':
                # TODO Adicionar os campos vBCSTRet, pST e vICMSSTRet futuramente
                imposto['ICMS'].update({
                    'vICMSSubstituto': "%.02f" % item.icms_substituto,
                })

            if self.finalidade_emissao[0] == '4':
                # Devolução de IPI
                imposto['IPI'] = {}

                impostoDevol = {
                    'pDevol': "%.02f" % 100,
                    'vIPIDevol': "%.02f" % item.ipi_valor,
                }
            else:
                imposto['IPI'] = {
                    'clEnq': item.classe_enquadramento_ipi or '',
                    'cEnq': item.codigo_enquadramento_ipi,
                    'CST': item.ipi_cst,
                    'vBC': "%.02f" % item.ipi_base_calculo,
                    'pIPI': "%.02f" % item.ipi_aliquota,
                    'vIPI': "%.02f" % item.ipi_valor,
                }

        # Para casos de emissão de NFe conjugada, não
        # temos ICMS, IPI e II
        if item.tipo_produto == 'service':
            imposto['ISSQN'] = {
                'vBC': "%.02f" % item.issqn_base_calculo,
                'vAliq': "%.02f" % item.issqn_aliquota,
                'vISSQN': "%.02f" % item.issqn_valor,
                'cMunFG': "%s%s" % (partner.state_id.ibge_code, partner.city_id.ibge_code),  # noqa
                'cListServ': fiscal_position.service_type_id.code,
                'indISS': item.ind_iss,
                'indIncentivo': item.ind_incentivo,
            }

            # Informar somente quando declarada a suspensão da
            # exigibilidade do ISSQN.
            if item.ind_iss in ('6', '7'):
                imposto['ISSQN']['nProcesso'] = item.n_processo

        imposto['PIS'] = {
            'CST': item.pis_cst,
            'vBC': "%.02f" % item.pis_base_calculo,
            'pPIS': "%.02f" % item.pis_aliquota,
            'vPIS': "%.02f" % item.pis_valor,
        }

        imposto['COFINS'] = {
            'CST': item.cofins_cst,
            'vBC': "%.02f" % item.cofins_base_calculo,
            'pCOFINS': "%.02f" % item.cofins_aliquota,
            'vCOFINS': "%.02f" % item.cofins_valor,
        }

        if item.tem_difal:
            imposto['ICMSUFDest'] = {
                'vBCUFDest': "%.02f" % item.icms_bc_uf_dest,
                'pFCPUFDest': "%.02f" % item.icms_aliquota_fcp_uf_dest,
                'pICMSUFDest': "%.02f" % item.icms_aliquota_uf_dest,
                'pICMSInter': "%.02f" % item.icms_aliquota_interestadual,
                'pICMSInterPart': "%.02f" % item.icms_aliquota_inter_part,
                'vFCPUFDest': "%.02f" % item.icms_fcp_uf_dest,
                'vICMSUFDest': "%.02f" % item.icms_uf_dest,
                'vICMSUFRemet': "%.02f" % item.icms_uf_remet,
            }

        # Se xProd for maior que 120 caracteres, o restante da descrição deve
        # ser concatenado ao campo InfAdProd
        inf_ad_prod = item.product_description[120:] + ' '
        inf_ad_prod += item.informacao_adicional if item.informacao_adicional else ''  # noqa

        return {
            'prod': prod,
            'imposto': imposto,
            'impostoDevol': impostoDevol,
            'infAdProd': inf_ad_prod[:500],
        }

    @api.multi
    def _prepare_electronic_invoice_values(self):
        res = super(InvoiceElectronic, self)._prepare_electronic_invoice_values()  # noqa: 501

        if self.model not in ('55', '65'):
            return res

        vals = {
            **res,
        }

        tz = pytz.timezone(self.env.user.partner_id.tz) or pytz.utc

        # Ajusta data para a timezone do usuario
        dt_emissao = pytz.utc.localize(self.data_emissao).astimezone(tz)
        dt_fatura = pytz.utc.localize(self.data_fatura).astimezone(tz)

        ide = {
            'cUF': self.company_id.state_id.ibge_code,
            'cNF': "%08d" % self.numero_controle,
            'natOp': self.fiscal_position_id.name,
            # 'mod': self.model,
            'serie': self.serie.code,
            'nNF': self.numero,
            'dhEmi': dt_emissao.strftime('%Y-%m-%dT%H:%M:%S-03:00'),
            'dhSaiEnt': dt_emissao.strftime('%Y-%m-%dT%H:%M:%S-03:00'),
            'tpNF': '0' if self.tipo_operacao == 'entrada' else '1',
            'idDest': self.ind_dest or 1,
            'cMunFG': "%s%s" % (self.company_id.state_id.ibge_code,
                                self.company_id.city_id.ibge_code),
            # Formato de Impressão do DANFE - 1 - Danfe Retrato, 4 - Danfe NFCe
            'tpImp': '1' if self.model == '55' else '4',
            # Tipo de Emissao para NFCe somente '9' ou '4' (dependendo do estado)
            'tpEmis': self.tipo_emissao,
            'tpAmb': 2 if self.ambiente == 'homologacao' else 1,
            # Pegamos o primeiro digito, porque começamos a usar subtipos de finalidade
            'finNFe': self.finalidade_emissao[0],
            'indFinal': self.ind_final or '1',
            'indPres': self.ind_pres or '1',
            'procEmi': 0,
            'verProc': 'Multidados-12.0',
        }

        if self.model == '65':

            ide.update({
                'tpEmis': '1',
                'idDest': '1',
                'finfe': '1',
                'indFinal': '1',
                'indPres': '1',
            })

        if self.ind_pres in ('2', '3', '4', '9'):
            ide['indIntermed'] = self.ind_intermed

        # Documentos Relacionados
        documentos = []
        for doc in self.fiscal_document_related_ids:
            data = fields.Datetime.from_string(doc.date)

            if doc.document_type == 'nfe':
                documentos.append({
                    'refNFe': doc.access_key
                })

            elif doc.document_type == 'nf':
                documentos.append({
                    'refNF': {
                        'cUF': doc.state_id.ibge_code,
                        'AAMM': data.strftime("%y%m"),
                        'CNPJ': re.sub('[^0-9]', '', doc.cnpj_cpf),
                        'mod': doc.fiscal_document_id.code,
                        'serie': doc.serie,
                        'nNF': doc.internal_number,
                    }
                })

            elif doc.document_type == 'cte':
                documentos.append({
                    'refCTe': doc.access_key
                })

            elif doc.document_type == 'nfrural':
                cnpj_cpf = re.sub('[^0-9]', '', doc.cnpj_cpf)

                documentos.append({
                    'refNFP': {
                        'cUF': doc.state_id.ibge_code,
                        'AAMM': data.strftime("%y%m"),
                        'CNPJ': cnpj_cpf if len(cnpj_cpf) == 14 else '',
                        'CPF': cnpj_cpf if len(cnpj_cpf) == 11 else '',
                        'IE': doc.inscr_est,
                        'mod': doc.fiscal_document_id.code,
                        'serie': doc.serie,
                        'nNF': doc.internal_number,
                    }
                })

            elif doc.document_type == 'cf':
                documentos.append({
                    'refECF': {
                        'mod': doc.fiscal_document_id.code,
                        'nECF': doc.serie,
                        'nCOO': doc.internal_number,
                    }
                })

        ide['NFref'] = documentos

        emit = {
            'tipo': self.company_id.partner_id.company_type,
            'cnpj_cpf': re.sub('[^0-9]', '', self.company_id.cnpj_cpf),
            'xNome': self.company_id.legal_name,
            'xFant': self.company_id.name,
            'enderEmit': {
                'xLgr': self.company_id.street,
                'xCpl': self.company_id.street2 or '',
                'nro': self.company_id.number,
                'xBairro': self.company_id.district,
                'cMun': '%s%s' % (self.company_id.partner_id.state_id.ibge_code,  # noqa: 501
                                  self.company_id.partner_id.city_id.ibge_code),  # noqa: 501
                'xMun': self.company_id.city_id.name,
                'UF': self.company_id.state_id.code,
                'CEP': re.sub('[^0-9]', '', self.company_id.zip),
                'cPais': self.company_id.country_id.ibge_code,
                'xPais': self.company_id.country_id.name,
                'fone': re.sub('[^0-9]', '', self.company_id.phone or '')
            },
            'IE': re.sub('[^0-9]', '', self.company_id.inscr_est),
            'CRT': self.company_id.fiscal_type,
        }

        if self.company_id.cnae_main_id and self.company_id.inscr_mun:
            emit['IM'] = re.sub('[^0-9]', '', self.company_id.inscr_mun or '')
            emit['CNAE'] = re.sub('[^0-9]', '', self.company_id.cnae_main_id.code or '')  # noqa: 501
            emit['CNAE'] = emit['CNAE'].zfill(7)

        dest = None
        exporta = None

        if self.commercial_partner_id:
            partner = self.commercial_partner_id

            dest = {
                'tipo': partner.company_type,
                'cnpj_cpf': re.sub('[^0-9]', '', partner.cnpj_cpf or ''),
                'xNome': partner.legal_name or partner.name,
                'enderDest': {
                    'xLgr': partner.street,
                    'xCpl': partner.street2 or '',
                    'nro': partner.number,
                    'xBairro': partner.district,
                    'cMun': '%s%s' % (partner.state_id.ibge_code,
                                      partner.city_id.ibge_code),
                    'xMun': partner.city_id.name,
                    'UF': partner.state_id.code,
                    'CEP': re.sub('[^0-9]', '', partner.zip or ''),
                    'cPais': (partner.country_id.bc_code or '')[-4:],
                    'xPais': partner.country_id.name,
                    'fone': re.sub('[^0-9]', '', partner.phone or '')
                },
                'indIEDest': self.ind_ie_dest,
                'IE': re.sub('[^0-9]', '', partner.inscr_est or ''),
            }

            if self.model == '65':

                dest.update({
                    'CPF': re.sub('[^0-9]', '', partner.cnpj_cpf or ''),
                    'IE': '',
                })

            if self.ambiente == 'homologacao':
                dest['xNome'] = 'NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL'  # noqa: 501

            if partner.country_id.id != self.company_id.country_id.id:
                dest['idEstrangeiro'] = re.sub('[^0-9]', '', partner.cnpj_cpf or '')  # noqa: 501
                dest['enderDest']['UF'] = 'EX'
                dest['enderDest']['xMun'] = 'Exterior'
                dest['enderDest']['cMun'] = '9999999'

                exporta = {
                    'UFSaidaPais': self.uf_saida_pais_id.code or '',
                    'xLocExporta': self.local_embarque or '',
                    'xLocDespacho': self.local_despacho or '',
                }

        if self.partner_shipping_id and self.partner_shipping_id != self.partner_id:

            partner = self.partner_shipping_id

            # Quando o partner é do tipo endereço de entrega
            # nos utilizamos o cnpj e nome da empresa pai
            if partner.type == 'delivery':
                name = partner.parent_id.legal_name or partner.parent_id.name
                cnpj_cpf = partner.parent_id.cnpj_cpf
                is_company = partner.parent_id.is_company
            else:
                name = partner.legal_name or partner.name
                cnpj_cpf = partner.cnpj_cpf
                is_company = partner.is_company

            # Ajusta Inscrição Estadual de Acordo com o Cadastro
            # do Endereço
            if partner.indicador_ie_dest == '1':
                if partner.inscr_est != '':
                    inscr_est = partner.parent_id.inscr_est
                else:
                    inscr_est = partner.inscr_est
            else:
                inscr_est = ''

            entrega = {
                'xNome': name,
                'xLgr': partner.street or '',
                'nro': partner.number,
                'xCpl': partner.street2 or '',
                'xBairro': partner.district,
                'cMun': '%s%s' % (partner.state_id.ibge_code, partner.city_id.ibge_code),  # noqa
                'xMun': partner.city_id.name,
                'UF': partner.state_id.code,
                'CEP': re.sub('[^0-9]', '', partner.zip or ''),
                'cPais': (partner.country_id.bc_code or '')[-4:],
                'xPais': partner.country_id.name,
                'fone': re.sub('[^0-9]', '', partner.phone or ''),
                'email': partner.email or '',
                'IE': re.sub('[^0-9]', '', inscr_est or ''),
            }

            if is_company:
                entrega['CNPJ'] = re.sub('[^0-9]', '', cnpj_cpf or '')
            else:
                entrega['CPF'] = re.sub('[^0-9]', '', cnpj_cpf or '')

            vals['entrega'] = entrega

        autorizados = []

        if self.company_id.accountant_id:
            autorizados.append({
                'CNPJ': re.sub(
                    '[^0-9]', '', self.company_id.accountant_id.cnpj_cpf)
            })

        electronic_items = []

        for item in self.electronic_item_ids:
            electronic_items.append(
                self._prepare_electronic_invoice_item(item, self))

        total = {
            # ICMS
            'vBC': "%.02f" % self.valor_bc_icms,
            'vICMS': "%.02f" % self.valor_icms,
            'vICMSDeson': '0.00',
            'vFCPST': '0.00',
            'vFCP': '0.00',
            'vFCPSTRet': '0.00',
            'vIPIDevol': "%.02f" % self.valor_ipi if self.finalidade_emissao[0] == '4' else '0.00',
            'vBCST': "%.02f" % self.valor_bc_icmsst,
            'vST': "%.02f" % self.valor_icmsst,
            'vProd': "%.02f" % (self.valor_bruto - self.valor_servicos),
            'vFrete': "%.02f" % self.valor_frete,
            'vSeg': "%.02f" % self.valor_seguro,
            'vDesc': "%.02f" % self.valor_desconto,
            'vII': "%.02f" % self.valor_ii,
            'vIPI': "%.02f" % self.valor_ipi if self.finalidade_emissao[0] != '4' else '0.00',
            'vPIS': "%.02f" % (self.valor_pis - self.valor_pis_servicos),
            'vCOFINS': "%.02f" % (self.valor_cofins - self.valor_cofins_servicos),  # noqa
            'vOutro': "%.02f" % self.valor_despesas,
            'vNF': "%.02f" % self.valor_final,
            'vFCPUFDest': "%.02f" % self.valor_icms_fcp_uf_dest,
            'vICMSUFDest': "%.02f" % self.valor_icms_uf_dest,
            'vICMSUFRemet': "%.02f" % self.valor_icms_uf_remet,
            'vTotTrib': "%.02f" % self.valor_estimado_tributos,
        }

        issqn_total = {
            # ISSQn
            'vServ': "%.02f" % self.valor_servicos if self.valor_servicos else '',
            'vBC': "%.02f" % self.valor_bc_issqn if self.valor_bc_issqn else '',
            'vISS': "%.02f" % self.valor_issqn if self.valor_issqn else '',
            'vPIS': "%.02f" % self.valor_pis_servicos if self.valor_pis_servicos else '',
            'vCOFINS': "%.02f" % self.valor_cofins_servicos if self.valor_cofins_servicos else '',
            'dCompet': dt_fatura.strftime('%Y-%m-%d'),
            'vDeducao': '',
            'vOutro': '',
            'vDescIncond': '',
            'vDescCond': '',
            'vISSRet': "%.02f" % self.valor_retencao_issqn if self.valor_retencao_issqn else '',
            'cRegTrib': '',
        }

        transp = {
            'modFrete': self.modalidade_frete,
            'transporta': {
                'xNome': (self.transportadora_id.legal_name or
                          self.transportadora_id.name or ''),
                'IE': re.sub('[^0-9]', '',
                             self.transportadora_id.inscr_est or ''),
                'xEnder': "%s - %s, %s" % (self.transportadora_id.street,
                                           self.transportadora_id.number,
                                           self.transportadora_id.district)
                if self.transportadora_id else '',
                'xMun': self.transportadora_id.city_id.name or '',
                'UF': self.transportadora_id.state_id.code or ''
            },
            'veicTransp': {
                'placa': self.placa_veiculo or '',
                'UF': self.uf_veiculo or '',
                'RNTC': self.rntc or '',
            }
        }

        cnpj_cpf = re.sub('[^0-9]', '', self.transportadora_id.cnpj_cpf or '')

        if self.transportadora_id.is_company:
            transp['transporta']['CNPJ'] = cnpj_cpf
        else:
            transp['transporta']['CPF'] = cnpj_cpf

        reboques = []

        for item in self.reboque_ids:
            reboques.append({
                'placa': item.placa_veiculo or '',
                'UF': item.uf_veiculo or '',
                'RNTC': item.rntc or '',
                'vagao': item.vagao or '',
                'balsa': item.balsa or '',
            })

        transp['reboque'] = reboques
        volumes = []

        for item in self.volume_ids:
            volumes.append({
                'qVol': item.quantidade_volumes or '',
                'esp': item.especie or '',
                'marca': item.marca or '',
                'nVol': item.numeracao or '',
                'pesoL': "%.03f" % item.peso_liquido
                if item.peso_liquido else '',
                'pesoB': "%.03f" % item.peso_bruto if item.peso_bruto else '',
            })

        transp['vol'] = volumes

        duplicatas = []

        for dup in self.duplicata_ids:

            if dup.data_vencimento:
                vencimento = fields.Datetime.from_string(dup.data_vencimento)
                duplicatas.append({
                    'nDup': dup.numero_duplicata,
                    'dVenc': vencimento.strftime('%Y-%m-%d'),
                    'vDup': "%.02f" % dup.valor,
                })

        cobr = {
            'fat': {
                'nFat': self.numero_fatura or '',
                'vOrig': "%.02f" % (self.fatura_bruto or 0.00),
                'vDesc': "%.02f" % (self.fatura_desconto or 0.00),
                'vLiq': "%.02f" % (self.fatura_liquido or 0.00),
            },
        }

        # Ordenamos em ordem crescente as duplicadas de acordo com o numero
        # das mesmas para evitar erro no SEFAZ
        if duplicatas:
            duplicatas.sort(key=lambda dup: dup['nDup'])
            cobr['dup'] = duplicatas

        det_pag_group = []
        compras = {}

        if self.model != '65':

            # Foi utilizado a 14 para a tag 'tPag' porque duplicata
            # mercantil permite o pagemento de varias formas.

            # Para NFe de Simples Remessa, Complementar, Devolução ou Ajuste, temos os seguintes valores
            # tPag '90' indica 'Sem Pagamento'
            if self.fiscal_position_id.finalidade_emissao in ('1.1', '3', '4') or self.finalidade_emissao == '2':

                det_pag_group.append({
                    'tPag': '90',
                    'vPag': '0.00',
                })

            else:

                for parcel in self.invoice_id.parcel_ids:

                    t_pag = parcel.title_type_id.nfe_tpag

                    det_pag_group.append({
                        'indPag': self.payment_term_id.indPag or '0',
                        'tPag': t_pag,
                        'vPag': "%.02f" % parcel.parceling_value if t_pag != '90' else '0.00',
                    })

            pag = {
                'detPag': det_pag_group,
            }

            compras.update({
                'xNEmp': self.nota_empenho or '',
                'xPed': self.pedido_compra or '',
                'xCont': self.contrato_compra or '',
            })

        else:

            pagamentos = self.statement_ids.filtered(lambda r: r.amount >= 0)
            troco = self.statement_ids - pagamentos

            for pagamento in pagamentos:

                det_pag_group.append({
                    'indPag': self.payment_term_id.indPag or '0',
                    'tPag': pagamento.title_type_id.nfe_tpag or '01',
                    'vPag': '%.02f' % pagamento.amount or 0.0,
                })

            pag = {
                'detPag': det_pag_group,
                'vTroco': '%.02f' % abs(troco.amount) if troco else '0.00',
            }

            ambiente = 1 if self.ambiente == 'producao' else 2

            estado = self.company_id.state_id.ibge_code

            cid_token = int(self.company_id.id_token_csc)
            csc = self.company_id.csc

            hash_qr_code = "{0}|2|{1}|{2}{3}".format(self.chave_nfe, ambiente, cid_token, csc)  # noqa
            hash_qr_code = hashlib.sha1(hash_qr_code.encode()).hexdigest()

            qr_code_url = "p={0}|2|{1}|{2}|{3}".format(self.chave_nfe, ambiente, cid_token, hash_qr_code)  # noqa
            qr_code_server = url_qrcode(estado, str(ambiente))

            qrcode_url = qr_code_server + qr_code_url
            chave_url = url_qrcode_exibicao(estado, str(ambiente))

            vals.update({
                'qrCode': qrcode_url,
                'urlChave': chave_url,
            })

            self.write({
                'qrcode_url': qrcode_url,
                'chave_url': chave_url,
            })

        infAdic = {
            'infCpl': self.informacoes_complementares or '',
            'infAdFisco': self.informacoes_legais[:2000] if self.informacoes_legais else '',
        }

        # Informacoes do responsavel tecnico
        resp_tecnico = self.company_id.resp_tecnico_id

        if not resp_tecnico:
            raise UserError('Cadastro de Responsável Técnico ausente. Contate administrador do sistema.')  # noqa

        inf_resp_tec = {
            'CNPJ': re.sub('[^0-9]', '', resp_tecnico.cnpj),
            'xContato': resp_tecnico.name,
            'email': resp_tecnico.email,
            'fone': re.sub('[^0-9]', '', resp_tecnico.phone),
        }

        vals_ext = {
            'Id': '',
            'ide': ide,
            'emit': emit,
            'dest': dest,
            'autXML': autorizados,
            'detalhes': electronic_items,
            'total': total,
            'ISSQNtot': issqn_total,
            'pag': pag,
            'transp': transp,
            'infAdic': infAdic,
            'exporta': exporta,
            'compra': compras,
            'infRespTec': inf_resp_tec,
        }

        vals.update(vals_ext)

        if self.ind_intermed == '1':

            vals['infIntermed'] = {
                'CNPJ': re.sub('[^0-9]', '', self.cnpj_intermed),
                'idCadIntTran': self.id_cad_int_tran,
            }

        if len(duplicatas) > 0:
            vals['cobr'] = cobr

        return vals

    @api.multi
    def _prepare_lote(self, lote, nfe_values):

        values = {
            'idLote': lote,
            'indSinc': 1 if self.model == '65' else 0,
            'estado': self.company_id.partner_id.state_id.ibge_code,
            'ambiente': 1 if self.ambiente == 'producao' else 2,
            'modelo': self.model,
            'NFes': [{
                'infNFe': nfe_values,
            }]
        }
        return values

    def _gerar_chave_nfe(self):
        """Gera chave para autenticacao da NFe
        """

        for edoc in self:

            if edoc.model not in ('55', '65'):
                continue

            data_emissao = edoc.data_emissao.strftime(
                '%Y-%m-%dT%H:%M:%S-00:00')

            chave_dict = {
                'cnpj': re.sub('[^0-9]', '', edoc.company_id.cnpj_cpf),
                'estado': edoc.company_id.state_id.ibge_code,
                'emissao': data_emissao[2:4] + data_emissao[5:7],
                'modelo': edoc.model,
                'numero': edoc.numero,
                'serie': edoc.serie.code.zfill(3),
                'tipo': int(edoc.tipo_emissao),
                'codigo': "%08d" % edoc.numero_controle,
            }

            edoc.chave_nfe = gerar_chave(ChaveNFe(**chave_dict))

    @api.multi
    def action_post_validate(self):
        super(InvoiceElectronic, self).action_post_validate()
        self._gerar_chave_nfe()

    @api.multi
    def action_send_electronic_invoice(self):
        """Realiza o envio dos doc. eletronicos que são
        NFe de Venda - do tipo '55' e '65'
        """
        super(InvoiceElectronic, self).action_send_electronic_invoice()

        for rec in self:

            if rec.model not in ('55', '65') or rec.state in ('done', 'denied', 'cancel'):  # noqa
                continue

            rec.write({
                'state': 'error',
                'data_emissao': datetime.now(),
            })

            # Como a data de emissao foi renovada
            # devemos gerar a chave novamente para que ela seja
            # geradao com os dados atualizados
            rec._gerar_chave_nfe()

            nfe_values = rec._prepare_electronic_invoice_values()
            lote = rec._prepare_lote(rec.id, nfe_values)

            cert = rec.company_id.with_context({'bin_size': False}).nfe_a1_file  # noqa
            cert_pfx = base64.decodestring(cert)

            certificado = Certificado(cert_pfx, rec.company_id.nfe_a1_password)  # noqa

            xml_enviar = xml_autorizar_nfe(certificado, **lote)
            mensagens_erro = valida_nfe(xml_enviar)

            if mensagens_erro:

                # Criamos um evento para sinalizar que a NFe esta com ERRO
                self.env['invoice.electronic.event'].create({
                    'code': 'ERRO',
                    'name': mensagens_erro,
                    'invoice_electronic_id': rec.id,
                })

                rec.write({
                    'codigo_retorno': '',
                    'mensagem_retorno': mensagens_erro,
                })


                continue

            try:

                resposta = autorizar_nfe(certificado,
                                         xml=xml_enviar,
                                         estado=rec.company_id.state_id.ibge_code,
                                         ambiente=1 if rec.ambiente == 'producao' else 2,
                                         modelo=rec.model)

            except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError) as exec:

                msg = """Erro de Timeout na requisição: Não foi possivel se conectar ao SEFAZ.
                O SEFAZ pode estar offline ou sofrendo instabilidade em sua conexão.
                Por favor, tente mais tarde."""

                # Criamos um evento para sinalizar que a NFe esta com ERRO de timeout
                self.env['invoice.electronic.event'].create({
                    'code': 'TIMEOUT',
                    'name': msg,
                    'invoice_electronic_id': rec.id,
                    'category': 'info',
                })

                rec.write({
                    'codigo_retorno': 'TIMEOUT',
                    'mensagem_retorno': msg,
                    'state': 'draft',
                })

                continue

            retorno = resposta['object'].getchildren()[0]

            if retorno.cStat == 103:

                obj = {
                    'estado': rec.company_id.partner_id.state_id.ibge_code,
                    'ambiente': 1 if rec.ambiente == 'producao' else 2,
                    'modelo': rec.model,
                    'obj': {
                        'ambiente': 1 if rec.ambiente == 'producao' else 2,
                        'numero_recibo': retorno.infRec.nRec
                    }
                }

                rec.recibo_nfe = obj['obj']['numero_recibo']
                resposta_recibo = None

                while True:
                    time.sleep(5)
                    resposta_recibo = retorno_autorizar_nfe(certificado, **obj)  # noqa
                    retorno = resposta_recibo['object'].getchildren()[0]

                    if retorno.cStat != 105:
                        break

            else:
                resposta_recibo = None

            if retorno.cStat != 104:

                values = {
                    'codigo_retorno': retorno.cStat,
                    'mensagem_retorno': retorno.xMotivo,
                }

            else:

                values = {
                    'codigo_retorno': retorno.protNFe.infProt.cStat,
                    'mensagem_retorno': retorno.protNFe.infProt.xMotivo,
                }

                if values['codigo_retorno'] == 100:

                    values.update({
                        'state': 'done',
                        'protocolo_nfe': retorno.protNFe.infProt.nProt,
                        'data_autorizacao': retorno.protNFe.infProt.dhRecbto,
                    })

                # Duplicidade de NF-e significa que a nota já está emitida
                # Busca protocolo da NFe e verifica sua atual situação
                elif values['codigo_retorno'] == 204:

                    # Criamos um evento para sinalizar que a NFe esta duplicada no SEFAZ
                    self.env['invoice.electronic.event'].create({
                        'code': values['codigo_retorno'],
                        'name': values['mensagem_retorno'],
                        'invoice_electronic_id': rec.id,
                    })

                    # Consultamos o protocolo
                    resposta_cons_prot = rec._get_protocolo_nfe()

                    # Atualiza os valores de acordo com o retorno
                    # a consulta de protocolo
                    values.update({
                        'state': 'done',
                        **resposta_cons_prot,
                    })

                # Denegada e nota já está denegada
                elif values['codigo_retorno'] in (302, 205):

                    values.update({
                        'state': 'denied',
                    })

                    rec.set_invoice_denied()

            self.env['invoice.electronic.event'].create({
                'code': values['codigo_retorno'],
                'name': values['mensagem_retorno'],
                'invoice_electronic_id': rec.id,
            })

            rec._create_attachment('nfe-envio', rec, resposta['sent_xml'])
            rec._create_attachment('nfe-ret', rec, resposta['received_xml'])  # noqa

            if resposta_recibo:
                rec._create_attachment('rec', rec, resposta_recibo['sent_xml'])  # noqa
                rec._create_attachment('rec-ret', rec, resposta_recibo['received_xml'])  # noqa

                received_xml = resposta_recibo['received_xml']

            else:
                # Na NFce o envio da fatura e sincrono. Entao
                # nao temos uma segunda consulta para capturar o
                # recibo

                received_xml = resposta['received_xml']

            nfe_proc = gerar_nfeproc(resposta['sent_xml'], received_xml)  # noqa

            values.update({
                'nfe_processada': base64.encodestring(nfe_proc),
                'nfe_processada_name': "NFe%08d.xml" % rec.numero,
            })

            rec.write(values)

            if rec.codigo_retorno == '100':

                # Não sobrescrevemos o numero da fatura para
                # Nota Complementar. O novo numero e salvo apenas no
                # doc. eletronico relacionado
                if rec.finalidade_emissao != '2':
                    rec.invoice_id.internal_number = int(rec.numero)
                    rec.invoice_id.date_invoice = fields.Date.from_string(rec.data_autorizacao)
                else:
                    # Cria lançamentos de diario adicionais
                    # para os impostos da NFe Complementar
                    wiz = self.env['wizard.nfe.complementar'].create({
                        'edoc_id': rec.id,
                    })

                    wiz.create_edoc_complementar_move_line(rec)

    @api.multi
    def action_consultar_protocolo_nfe(self):
        """Realiza consulta do protocolo de uma NFe a partir
        da sua respectiva chave. O metodo preenche o numero de protoco,
        codigo de retorno e mensagem de retorno da situação atual da NFe

        """

        for rec in self:

            # Consultamos o protocolo da nfe
            values = rec._get_protocolo_nfe()

            # Salvamos os valoreas em casos de consulta de protocolo separado do
            # do envio da NFe
            rec.write(values)

    def _get_protocolo_nfe(self):
        """Realiza consulta do protocolo de uma NFe a partir
        da sua respectiva chave. Usado em casos de erro na consulta
        onde o numero de protocolo fica vazio (erro 204, por exemplo).

        Returns:
            dict: Dict com os valores dos campos retornado pelo servico de consulta
        """

        for rec in self:

            if rec.model not in ('55', '65'):
                raise UserError(
                    "Metodo de consulta valido apenas para NFe do tipo '55' e '65'")

            cert = rec.company_id.with_context({'bin_size': False}).nfe_a1_file  # noqa
            cert_pfx = base64.decodestring(cert)

            certificado = Certificado(cert_pfx, rec.company_id.nfe_a1_password)  # noqa

            consulta_protocolo_vals = {
                'estado': rec.company_id.partner_id.state_id.ibge_code,
                'ambiente': 2 if rec.ambiente == 'homologacao' else 1,
                'modelo': rec.model,
                'obj': {
                    'chave_nfe': rec.chave_nfe,
                    'ambiente':  2 if rec.ambiente == 'homologacao' else 1,
                },
            }

            # Realiza consulta de protocolo da NFe a partir nda chave de acesso
            response = consultar_protocolo_nfe(certificado, **consulta_protocolo_vals)  # noqa
            response_obj = response['object'].getchildren()[0]

            # Salva numero do protocolo
            rec.protocolo_nfe = response_obj.protNFe.infProt.nProt

            # Salva o xml de envio e de retorno como anexo, para fins de documentacao
            rec._create_attachment('cons-protocolo-envio', rec, response['sent_xml'])  # noqa
            rec._create_attachment('cons-protocolo-ret', rec, response['received_xml'])  # noqa

            values = {
                'codigo_retorno': response_obj.protNFe.infProt.cStat,
                'mensagem_retorno': response_obj.protNFe.infProt.xMotivo,
                'protocolo_nfe': response_obj.protNFe.infProt.nProt,
            }

            return values

    @api.multi
    def generate_nfe_proc(self):
        if self.state in ['cancel', 'done', 'denied']:
            recibo = self.env['ir.attachment'].search([
                ('res_model', '=', 'invoice.electronic'),
                ('res_id', '=', self.id),
                ('datas_fname', 'like', 'rec-ret')])

            if not recibo:
                recibo = self.env['ir.attachment'].search([
                    ('res_model', '=', 'invoice.electronic'),
                    ('res_id', '=', self.id),
                    ('datas_fname', 'like', 'nfe-ret')])

            nfe_envio = self.env['ir.attachment'].search([
                ('res_model', '=', 'invoice.electronic'),
                ('res_id', '=', self.id),
                ('datas_fname', 'like', 'nfe-envio')])

            if nfe_envio.datas and recibo.datas:

                nfe_proc = gerar_nfeproc(
                    base64.decodestring(nfe_envio.datas),
                    base64.decodestring(recibo.datas)
                )

                self.nfe_processada = base64.encodestring(nfe_proc)
                self.nfe_processada_name = "NFe%08d.xml" % self.numero

        else:
            raise UserError('A NFe não está validada')

    @api.multi
    def action_back_to_draft(self):

        # NFe com codigo 155 ja ultrapassaram o periodo de cancelamento de devem ser canceladas
        # inicialmente na receita
        if self.state == 'error' and self.model in ('55', '65') and self.codigo_retorno == '155':
            raise UserError('NFe com codigo 155 devem ser canceladas diretamente pela prefeitura')

        super(InvoiceElectronic, self).action_back_to_draft()

    @api.multi
    def action_cancel_document(self, context=None, justificativa=None):

        res = super(InvoiceElectronic, self).action_cancel_document(context=context, justificativa=justificativa)  # noqa

        if self.model in ('55', '65'):

            if self.state == 'denied':
                raise UserError( "Não é possível cancelar NFe com status 'Denegado'.")

            if not self.protocolo_nfe and self.state == 'done':
                raise UserError(
                    "NFe sem Protocolo de Autorização. Por favor, utilize o botão 'Consultar Protocolo' para recuperá-lo.")

            if any(edoc_complementar.state == 'done' for edoc_complementar in self.complementar_ids):  # noqa
                raise UserError("""Este Doc. Eletronico possui uma nota complementar que ainda não foi cancelada.
                    Por favor, cancele-a primeiro para prosseguir com o cancelamento deste Doc. Eletrônico.""")

            if not justificativa:
                return {
                    'name': 'Cancelamento NFe',
                    'type': 'ir.actions.act_window',
                    'res_model': 'wizard.cancel.nfe',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {
                        'default_edoc_id': self.id,
                    }
                }

            cert = self.company_id.with_context({'bin_size': False}).nfe_a1_file  # noqa
            cert_pfx = base64.decodestring(cert)
            certificado = Certificado(cert_pfx, self.company_id.nfe_a1_password)  # noqa

            id_canc = "ID110111%s%02d" % (self.chave_nfe, self.sequencial_evento)  # noqa

            cancelamento = {
                'idLote': self.id,
                'estado': self.company_id.state_id.ibge_code,
                'ambiente': 2 if self.ambiente == 'homologacao' else 1,
                'modelo': self.model,
                'eventos': [{
                    'Id': id_canc,
                    'cOrgao': self.company_id.state_id.ibge_code,
                    'tpAmb': 2 if self.ambiente == 'homologacao' else 1,
                    'CNPJ': re.sub('[^0-9]', '', self.company_id.cnpj_cpf),
                    'chNFe': self.chave_nfe,
                    'dhEvento': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S-00:00'),  # noqa
                    'nSeqEvento': self.sequencial_evento,
                    'nProt': self.protocolo_nfe,
                    'xJust': justificativa,
                    'tpEvento': '110111',
                    'descEvento': 'Cancelamento',
                }]
            }

            resp = recepcao_evento_cancelamento(certificado, **cancelamento)
            resposta = resp['object'].retEnvEvento

            if resposta.cStat == 128 and resposta.retEvento.infEvento.cStat in (135, 136, 155):  # noqa: 501

                if resposta.retEvento.infEvento.cStat in (135, 136):
                    state = 'cancel'
                else:
                    # Se codigo de retorno for 155 -cancelamento homolgado fora do prazo
                    state = 'error'

                values = {
                    'state': state,
                    'codigo_retorno': resposta.retEvento.infEvento.cStat,
                    'mensagem_retorno': resposta.retEvento.infEvento.xMotivo,
                    'sequencial_evento': self.sequencial_evento + 1,
                }

                # Apenas para NFe Complementar
                if self.finalidade_emissao == '2':
                    # Excluir os lançamentos de diario adicionais
                    # para os impostos da NFe Complementar
                    wiz = self.env['wizard.nfe.complementar'].create({
                        'edoc_id': self.id,
                    })

                    wiz.cancel_nfe_complementar(self.id)

            elif resposta.cStat == 128:
                values = {
                    'codigo_retorno': resposta.retEvento.infEvento.cStat,
                    'mensagem_retorno': resposta.retEvento.infEvento.xMotivo,
                }

            else:
                values = {
                    'codigo_retorno': resposta.cStat,
                    'mensagem_retorno': resposta.xMotivo,
                }

            self.write(values)

            self.env['invoice.electronic.event'].create({
                'code': self.codigo_retorno,
                'name': self.mensagem_retorno,
                'invoice_electronic_id': self.id,
            })

            self._create_attachment('canc', self, resp['sent_xml'])
            self._create_attachment('canc-ret', self, resp['received_xml'])

        return res

    @api.multi
    def action_print_einvoice_report(self):

        nfe_docs = self.filtered(lambda r: r.model == '55')

        if nfe_docs:
            return self.env.ref('br_nfe.report_br_nfe_danfe').report_action(nfe_docs)

        nfce_docs = self.filtered(lambda r: r.model == '65')

        if nfce_docs:
            return self.env.ref('br_nfe.report_br_nfe_danfce').report_action(nfce_docs)

        return super(InvoiceElectronic, self).action_print_einvoice_report()

    @api.multi
    def action_generate_nfe_complementar(self):
        """Invoca wizard para criacao da NFe Complementar

        Returns:
            dict: dict com valores da action que invoca a wizard
        """

        return {
            'name': 'NFe Complementar',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.nfe.complementar',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_edoc_id': self.id,
                'default_invoice_id': self.invoice_id.id,
                'default_chave_nfe': self.chave_nfe,
            }
        }

    def _get_qr_code_image(self):
        """Gera QRCode para NFCe

        Returns:
            str: string base64 do QRCode para impressao de imagem
        """

        if self.model != '65':
            return ''

        buffered = BytesIO()

        img = qrcode.make(self.qrcode_url)
        img.save(buffered, format='JPEG')

        qrcode_img = base64.b64encode(buffered.getvalue())

        return qrcode_img

    def set_invoice_denied(self):

        for rec in self:
            rec.state = 'denied'
            rec.invoice_id._invoice_denied()
