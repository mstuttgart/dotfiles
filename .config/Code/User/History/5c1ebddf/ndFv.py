# © 2016 Danimar Ribeiro <danimaribeiro@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re
import pytz
import base64
import time
import logging
import urllib3
import requests

from odoo import api, fields, models
from odoo.exceptions import UserError

from odoo.addons.br_nfse_ginfes.models.const import TIPORPS, NATUREZA_OPERACAO, TRIBUTACAO, INC_CULTURAL

_logger = logging.getLogger(__name__)

try:
    import pytrustnfe.nfse.ginfes
    import pytrustnfe.certificado
except ImportError:
    _logger.error('Cannot import pytrustnfe', exc_info=True)


STATE = {'edit': [('readonly', False)]}


class InvoiceElectronic(models.Model):
    _inherit = 'invoice.electronic'

    lote_code = fields.Char(string='Lote')

    webservice_nfse = fields.Selection(selection_add=[
        ('nfse_ginfes', 'Ginfes'),
    ])

    nfse_ginfes_tipo_rps = fields.Selection(
        selection=TIPORPS,
        string='Tipo de RPS (ginfes)',
    )

    nfse_ginfes_natureza_operacao = fields.Selection(
        selection=NATUREZA_OPERACAO,
        string='Natureza da Operação (ginfes)',
    )

    nfse_ginfes_regime_tributacao = fields.Selection(
        selection=TRIBUTACAO,
        string='Regime de Tributação (ginfes)',
        help='Código de identificação do regime especial de tributação',
    )

    nfse_ginfes_incentivador_cultural = fields.Selection(
        selection=INC_CULTURAL,
        string='Incentivador Cultural (ginfes)',
    )

    nfse_ginfes_emissor = fields.Selection(
        string='Emissor (ginfes)',
        selection=[
            ('ginfes', 'Ginfes'),
            ('fortaleza', 'Fortaleza'),
        ],
        default='ginfes',
        help="""Indica se o sistema de ginfes usado sera o padrão ou do município de Fortaleza""",
    )

    def _get_state_to_send(self):
        res = super(InvoiceElectronic, self)._get_state_to_send()
        return res + ('waiting',)

    @api.multi
    def _hook_validation(self):
        """Realiza validacao de campos criticos para emissao da NFSe.

        Returns:
            list: Lista de erros que detectados
        """

        errors = super(InvoiceElectronic, self)._hook_validation()

        if self.model == '001' and self.webservice_nfse == 'nfse_ginfes':

            issqn_codigo = ''

            if not self.company_id.inscr_mun:
                errors.append('Inscrição municipal obrigatória')

            if not self.company_id.cnae_main_id.code:
                errors.append('CNAE Principal da empresa obrigatório')

            if not self.codigo_tributacao_municipio:
                errors.append('Código de tributação do município obrigatório')

            if not self.company_id.cnae_main_id:
                errors.append('CNAE obrigatório')

            for eletr in self.electronic_item_ids:

                prod = "Produto: %s - %s" % (eletr.product_id.default_code,
                                             eletr.product_id.name)

                if eletr.tipo_produto == 'product':
                    errors.append('Esse documento permite apenas serviços - %s' % prod)  # noqa

                if eletr.tipo_produto == 'service':

                    if not eletr.issqn_codigo:
                        errors.append('%s - Código de Serviço' % prod)

                    if not issqn_codigo:
                        issqn_codigo = eletr.issqn_codigo

                    if issqn_codigo != eletr.issqn_codigo:
                        errors.append('%s - Apenas itens com o mesmo código de serviço podem ser enviados' % prod)  # noqa

            # altera api de emissao de acordo com o municipio

        return errors

    @api.multi
    def _prepare_electronic_invoice_values(self):
        """Monta dict com valores para montagem do XML para envio
        da NFSe

        Returns:
            dict: dicionario com os campos da NFSE
        """

        res = super(InvoiceElectronic, self)._prepare_electronic_invoice_values()  # noqa

        if self.model == '001' and self.webservice_nfse == 'nfse_ginfes':

            tz = pytz.timezone(self.env.user.partner_id.tz) or pytz.utc

            dt_emissao = pytz.utc.localize(self.data_emissao).astimezone(tz)
            dt_emissao = dt_emissao.strftime('%Y-%m-%dT%H:%M:%S')

            partner = self.commercial_partner_id
            city_tomador = partner.city_id

            tomador = {
                'tipo_cpfcnpj': 2 if partner.is_company else 1,
                'cnpj_cpf': re.sub('[^0-9]', '', partner.cnpj_cpf or ''),  # noqa
                'razao_social': partner.legal_name or partner.name,
                'logradouro': partner.street or '',
                'numero': partner.number or '',
                'complemento': partner.street2 or '',
                'bairro': partner.district or 'Sem Bairro',
                'cidade': '%s%s' % (city_tomador.state_id.ibge_code, city_tomador.ibge_code),  # noqa
                'uf': partner.state_id.code,
                'cep': re.sub('[^0-9]', '', partner.zip),
                # 'telefone': re.sub('[^0-9]', '', partner.phone or ''),
                'inscricao_municipal': re.sub('[^0-9]', '', partner.inscr_mun or ''),  # noqa
                'email': self.partner_id.email or partner.email or '',
            }

            city_prestador = self.company_id.partner_id.city_id

            prestador = {
                'cnpj': re.sub('[^0-9]', '', self.company_id.partner_id.cnpj_cpf or ''),  # noqa
                'inscricao_municipal': re.sub('[^0-9]', '', self.company_id.partner_id.inscr_mun or ''),  # noqa
                'cidade': '%s%s' % (city_prestador.state_id.ibge_code, city_prestador.ibge_code),  # noqa
                'cnae': re.sub('[^0-9]', '', self.company_id.cnae_main_id.code)
            }

            itens_servico = []

            descricao = []
            codigo_servico = ''

            for item in self.electronic_item_ids:

                descricao.append(item.name)

                itens_servico.append({
                    'descricao': item.name,
                    'quantidade': str("%.2f" % item.quantidade),
                    'valor_unitario': str("%.2f" % item.preco_unitario)
                })

                codigo_servico = item.issqn_codigo

            descricao = '\n'.join(descricao)

            rps = {
                'numero': self.numero_rps,
                'serie': self.serie.code or '',
                'tipo_rps': self.nfse_ginfes_tipo_rps,
                'data_emissao': dt_emissao,
                'natureza_operacao': self.nfse_ginfes_natureza_operacao,
                # 'regime_tributacao': self.nfse_ginfes_regime_tributacao,
                'optante_simples': '2' if self.company_id.fiscal_type == '3' else '1',  # noqa: 1 - Sim, 2 - Não
                'incentivador_cultural': self.nfse_ginfes_incentivador_cultural,
                'status': '1',  # 1 - Normal
                'valor_servico': str("%.2f" % self.valor_bruto),
                'valor_deducao': '0',
                'valor_pis': str("%.2f" % abs(self.valor_retencao_pis)),
                'valor_cofins': str("%.2f" % abs(self.valor_retencao_cofins)),
                'valor_inss': str("%.2f" % abs(self.valor_retencao_inss)),
                'valor_ir': str("%.2f" % abs(self.valor_retencao_irrf)),
                'valor_csll': str("%.2f" % abs(self.valor_retencao_csll)),
                'iss_retido': '1' if self.valor_retencao_issqn > 0 else '2',
                'valor_iss': str("%.2f" % abs(self.valor_issqn)),
                'valor_iss_retido': str("%.2f" % abs(self.valor_retencao_issqn)),
                'base_calculo': str("%.2f" % (self.valor_bruto - self.valor_desconto)),
                'aliquota_issqn': str("%.4f" % (self.electronic_item_ids[0].issqn_aliquota / 100)),  # noqa
                'valor_liquido_nfse': str("%.2f" % self.financial_price_total),
                'codigo_servico': codigo_servico,
                'codigo_tributacao_municipio': re.sub('[^0-9]', '', self.codigo_tributacao_municipio),  # noqa
                'descricao': descricao,
                'codigo_municipio': prestador['cidade'],
                'itens_servico': itens_servico,
                'tomador': tomador,
                'prestador': prestador,
            }

            nfse_vals = {
                'numero_lote': self.id,
                'inscricao_municipal': prestador['inscricao_municipal'],
                'cnpj_prestador': prestador['cnpj'],
                'lista_rps': [rps],
            }

            res.update(nfse_vals)
            res = pytrustnfe.utils.remove_especial_characters(res)

        return res

    @api.multi
    def action_back_to_draft(self):
        """ Retorna edoc para draft em casos de erro no envio de lote """
        super(InvoiceElectronic, self).action_back_to_draft()

        if self.model == '001' and self.webservice_nfse == 'nfse_ginfes':

            self.write({
                'codigo_retorno': '1',
                'mensagem_retorno': 'Aguardando envio',
                'state': 'draft',
            })

    @api.multi
    def action_send_electronic_invoice(self):
        """Realiza o envio de doc. eletronicos do NFSe Paulistana.
        O envio é realizado de forma assincrona. A
        """

        super(InvoiceElectronic, self).action_send_electronic_invoice()

        for rec in self:

            if rec.model == '001' and rec.webservice_nfse == 'nfse_ginfes' and rec.state == 'draft':

                rec.state = 'error'

                nfse_values = rec._prepare_electronic_invoice_values()

                cert = rec.company_id.with_context({'bin_size': False}).nfe_a1_file  # noqa
                cert_pfx = base64.decodestring(cert)

                certificado = pytrustnfe.certificado.Certificado(
                    cert_pfx, rec.company_id.nfe_a1_password)

                recebe_lote = None

                rec.lote_code = nfse_values['numero_lote']

                xml_enviar = pytrustnfe.nfse.ginfes.xml_recepcionar_lote_rps(certificado, nfse=nfse_values, emissor=rec.nfse_ginfes_emissor)

                # salva xml de envio para referencia em caso de erro
                rec.xml_to_send = base64.encodestring(xml_enviar.encode('utf-8'))  # noqa

                rec.xml_to_send_name = 'nfse-enviar-%s.xml' % rec.numero

                try:

                    recebe_lote = pytrustnfe.nfse.ginfes.recepcionar_lote_rps(
                        certificado, nfse=nfse_values, ambiente=rec.ambiente, emissor=rec.nfse_ginfes_emissor)

                except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):

                    msg = """Erro de Timeout na requisição: Não foi possivel se conectar ao GINFES.
                    O GINFES pode estar offline ou sofrendo instabilidade em sua conexão.
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

                retorno = recebe_lote['object']

                self._create_attachment('nfse-envio', rec, recebe_lote['sent_xml'])  # noqa
                self._create_attachment('nfse-envio-ret', rec, recebe_lote['received_xml'])  # noqa

                # Se o lote foi enviado de forma correta
                # e passa a aguardar processamento
                if 'NumeroLote' in dir(retorno):
                    rec.recibo_nfe = retorno.Protocolo
                    rec.state = 'open'
                    # Espera alguns segundos antes de consultar
                    time.sleep(5)
                else:
                    # Se o envio do lote apresentou erro
                    mensagem_retorno = retorno.ListaMensagemRetorno.MensagemRetorno  # noqa
                    rec.codigo_retorno = mensagem_retorno.Codigo
                    rec.mensagem_retorno = mensagem_retorno.Mensagem
                    rec.state = 'error'
                    continue

    def action_get_electronic_invoice_status(self):
        """Realiza consulta do status do RPS dos doc. eletronicos
        na prefeitura.
        """
        super(InvoiceElectronic, self).action_get_electronic_invoice_status()

        for rec in self:

            if rec.model == '001' and rec.recibo_nfe and rec.webservice_nfse == 'nfse_ginfes' and rec.state in ['open', 'error']:
                # Monta a consulta de situação do lote
                # 1 - Não Recebido
                # 2 - Não processado
                # 3 - Processado com erro
                # 4 - Processado com sucesso
                obj = {
                    'cnpj_prestador': re.sub('[^0-9]', '', rec.company_id.cnpj_cpf),
                    'inscricao_municipal': re.sub('[^0-9]', '', rec.company_id.inscr_mun),
                    'protocolo': rec.recibo_nfe,
                }

                cert = rec.company_id.with_context({'bin_size': False}).nfe_a1_file
                cert_pfx = base64.decodestring(cert)

                certificado = pytrustnfe.certificado.Certificado(cert_pfx, rec.company_id.nfe_a1_password)

                try:

                    consulta_situacao = pytrustnfe.nfse.ginfes.consultar_situacao_lote(
                        certificado, consulta=obj, ambiente=rec.ambiente, emissor=rec.nfse_ginfes_emissor)

                except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):

                    msg = """Erro de Timeout na requisição: Não foi possivel se conectar ao GINFES.
                    O GINFES pode estar offline ou sofrendo instabilidade em sua conexão.
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
                        'state': 'open',
                    })

                    continue

                ret_rec = consulta_situacao['object']

                vals = {}

                consulta_lote = None

                if "Situacao" in dir(ret_rec):

                    # Foi processado (independente do resultado)
                    if ret_rec.Situacao in (3, 4):

                        try:

                            consulta_lote = pytrustnfe.nfse.ginfes.consultar_lote_rps(
                                certificado, consulta=obj, ambiente=rec.ambiente, emissor=rec.nfse_ginfes_emissor)

                        except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):

                            msg = """Erro de Timeout na requisição: Não foi possivel se conectar ao GINFES.
                            O GINFES pode estar offline ou sofrendo instabilidade em sua conexão.
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
                                'state': 'open',
                            })

                            continue

                        ret_lote = consulta_lote['object']

                        # 4 - processado com sucesso
                        if "ListaNfse" in dir(ret_lote):

                            vals.update({
                                'state': 'done',
                                'codigo_retorno': '100',
                                'mensagem_retorno': 'NFSe emitida com sucesso',
                                'verify_code': ret_lote.ListaNfse.CompNfse.Nfse.InfNfse.CodigoVerificacao,  # noqa
                                'numero': ret_lote.ListaNfse.CompNfse.Nfse.InfNfse.Numero,
                                'data_autorizacao': fields.Date.to_string(fields.Date.context_today(self)),  # noqa
                            })

                        # RPS ja emitido
                        elif ret_lote.ListaMensagemRetorno.MensagemRetorno.Codigo == 'E10':

                            vals.update({
                                'state': 'error',
                                'codigo_retorno': ret_lote.ListaMensagemRetorno.MensagemRetorno.Codigo,  # noqa
                                'mensagem_retorno': ret_lote.ListaMensagemRetorno.MensagemRetorno.Mensagem,  # noqa
                            })

                            # edoc event para registrar que o erro ocorreu
                            self.env['invoice.electronic.event'].create({
                                'code': ret_lote.ListaMensagemRetorno.MensagemRetorno.Codigo,
                                'name': ret_lote.ListaMensagemRetorno.MensagemRetorno.Mensagem,
                                'invoice_electronic_id': rec.id,
                                'category': 'info',
                            })

                            vals.update(rec._consultar_nfse_rps_ginfes())

                        else:

                            # 3 - processado com erro
                            vals.update({
                                'state': 'error',
                                'codigo_retorno': ret_lote.ListaMensagemRetorno.MensagemRetorno.Codigo,  # noqa
                                'mensagem_retorno': ret_lote.ListaMensagemRetorno.MensagemRetorno.Mensagem,  # noqa
                            })

                    elif ret_rec.Situacao == 1:  # Reenviar caso não recebido

                        vals.update({
                            'codigo_retorno': '1',
                            'mensagem_retorno': 'Aguardando envio',
                            'state': 'draft',
                        })

                    else:
                        # recebido e aguardando processamento
                        vals.update({
                            'state': 'open',
                            'codigo_retorno': '2',
                            'mensagem_retorno': 'Lote aguardando processamento',
                        })

                else:
                    vals.update({
                        'state': 'error',
                        'codigo_retorno': ret_rec.ListaMensagemRetorno.MensagemRetorno.Codigo,
                        'mensagem_retorno': ret_rec.ListaMensagemRetorno.MensagemRetorno.Mensagem,
                    })

                rec.write(vals)

                self.env['invoice.electronic.event'].create({
                    'code': rec.codigo_retorno,
                    'name': rec.mensagem_retorno,
                    'invoice_electronic_id': rec.id,
                    'category': 'info',
                })

                if rec.state == 'done':
                    rec.invoice_id.internal_number = rec.numero

                if consulta_lote:
                    self._create_attachment('rec', rec, consulta_lote['sent_xml'])
                    self._create_attachment('rec-ret', rec, consulta_lote['received_xml'])

    @api.multi
    def action_cancel_document(self, context=None, justificativa=None):
        """Realiza cancelamento de lote de NFe. Como o sistema atualmente envia um RPS
        por lote, o cancelamento de lote representa em si o cancelamento do doc. eletronico
        na prefeitura.

        Args:
            context (dict, optional): Contexto com variaveis usados no metodo. Defaults to None.
            justificativa (str, optional): Justificativa para cancelamento da NFe. Defaults to None.

        Returns:
            bool: True, se a gravacao do metodo ocorreu de forma correta. False, caso contrario.
        """

        res = super(InvoiceElectronic, self).action_cancel_document(context=context, justificativa=justificativa)  # noqa

        if self.model == '001' and self.webservice_nfse == 'nfse_ginfes' and self.state == 'done':

            cert = self.company_id.with_context({'bin_size': False}).nfe_a1_file  # noqa
            cert_pfx = base64.decodestring(cert)

            certificado = pytrustnfe.certificado.Certificado(cert_pfx, self.company_id.nfe_a1_password)  # noqa

            company = self.company_id

            canc = {
                'cnpj_prestador': re.sub('[^0-9]', '', company.cnpj_cpf),
                'inscricao_municipal': re.sub('[^0-9]', '', company.inscr_mun),
                'numero_nfse': self.numero,
                'senha': company.senha_ambiente_nfse
            }

            try:

                # Para o cancelamento, ao contrario do que indica o manual, deve usar o
                # template V2 ao inves do V3, porque é o unico que funciona corretamente
                cancel = pytrustnfe.nfse.ginfes.cancelar_nfse(
                    certificado, cancelamento=canc, ambiente=self.ambiente, emissor=self.nfse_ginfes_emissor)

            except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):

                msg = """Erro de Timeout na requisição: Não foi possivel se conectar ao GINFES.
                    O GINFES pode estar offline ou sofrendo instabilidade em sua conexão.
                    Por favor, tente mais tarde."""

                # Criamos um evento para sinalizar que a NFe esta com ERRO de timeout
                self.env['invoice.electronic.event'].create({
                    'code': 'TIMEOUT',
                    'name': msg,
                    'invoice_electronic_id': self.id,
                    'category': 'info',
                })

                self.write({
                    'codigo_retorno': 'TIMEOUT',
                    'mensagem_retorno': msg,
                })

                return res

            retorno = cancel['object']

            vals = {}

            if retorno.Sucesso:

                vals.update({
                    'state': 'cancel',
                    'codigo_retorno': '100',
                    'mensagem_retorno': 'Nota Fiscal de Serviço Cancelada',
                })

            elif retorno.MensagemRetorno.Codigo == 'E79':
                # nota ja cancelada na prefeitura
                vals.update(self._consultar_nfse_rps_ginfes())

            else:

                vals.update({
                    'state': 'error',
                    'codigo_retorno': retorno.MensagemRetorno.Codigo,
                    'mensagem_retorno': retorno.MensagemRetorno.Mensagem,
                })

            self.write(vals)

            self.env['invoice.electronic.event'].create({
                'code': self.codigo_retorno,
                'name': self.mensagem_retorno,
                'invoice_electronic_id': self.id,
                'category': 'info',
            })

            self._create_attachment('canc', self, cancel['sent_xml'])
            self._create_attachment('canc-ret', self, cancel['received_xml'])

        return res

    @api.multi
    def action_consultar_nfse_rps_ginfes(self):
        """Metodo para ser utilizadao para consulta
        de dados da NFse.

        Returns:
            dict: campos do edoc com valores atualizados.
        """
        for rec in self:
            vals = rec._consultar_nfse_rps_ginfes()
            rec.write(vals)

    @api.multi
    def _consultar_nfse_rps_ginfes(self):
        """Consulta dados da NFSe já emitida ou cancelada.
        É possivel determinar se a NFSe esta ativa ou foi cancelada, bem
        como obter os dados da NFSe.

        Returns:
            dict: campos do edoc com valores atualizados.
        """

        if self.model != '001' or self.webservice_nfse != 'nfse_ginfes':
            return {}

        consulta = {
            'numero': self.numero_rps,
            'serie': self.serie.code or '',
            'tipo': self.nfse_ginfes_tipo_rps,
            'cnpj_prestador': re.sub('[^0-9]', '', self.company_id.partner_id.cnpj_cpf or ''),
            'inscricao_municipal': re.sub('[^0-9]', '', self.company_id.partner_id.inscr_mun or ''),
        }

        cert = self.company_id.with_context({'bin_size': False}).nfe_a1_file  # noqa
        cert_pfx = base64.decodestring(cert)

        certificado = pytrustnfe.certificado.Certificado(cert_pfx, self.company_id.nfe_a1_password)  # noqa

        try:

            consulta_nfse = pytrustnfe.nfse.ginfes.consultar_nfse_por_rps(
                certificado, consulta=consulta, ambiente=self.ambiente, emissor=self.nfse_ginfes_emissor)

        except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):

            msg = """Erro de Timeout na requisição: Não foi possivel se conectar ao GINFES.
            O GINFES pode estar offline ou sofrendo instabilidade em sua conexão.
            Por favor, tente mais tarde."""

            # Criamos um evento para sinalizar que a NFe esta com ERRO de timeout
            self.env['invoice.electronic.event'].create({
                'code': 'TIMEOUT',
                'name': msg,
                'invoice_electronic_id': self.id,
                'category': 'info',
            })

            return {
                'codigo_retorno': 'TIMEOUT',
                'mensagem_retorno': msg,
                'state': 'open',
            }

        ret_rec = consulta_nfse['object']

        # nfse cancelada na prefeitura
        if hasattr(ret_rec, 'CompNfse') and hasattr(ret_rec.CompNfse, 'NfseCancelamento'):

            vals = {
                'state': 'cancel',
                'codigo_retorno': '100',
                'mensagem_retorno': 'Nota Fiscal de Serviço Cancelada',
                'numero': ret_rec.CompNfse.Nfse.InfNfse.Numero,
                'data_autorizacao': ret_rec.CompNfse.Nfse.InfNfse.DataEmissao,
                'verify_code': ret_rec.CompNfse.Nfse.InfNfse.CodigoVerificacao,
            }

        # nfse presente na prefeitura mas nao cancelada
        elif hasattr(ret_rec, 'CompNfse') and hasattr(ret_rec.CompNfse, 'Nfse'):

            vals = {
                'state': 'done',
                'codigo_retorno': '100',
                'mensagem_retorno': 'Nota Fiscal emitida com sucesso',
                'numero': ret_rec.CompNfse.Nfse.InfNfse.Numero,
                'data_autorizacao': ret_rec.CompNfse.Nfse.InfNfse.DataEmissao,
                'verify_code': ret_rec.CompNfse.Nfse.InfNfse.CodigoVerificacao,
            }

        else:
            vals = {}

        return vals

    @api.multi
    def cron_send_nfe(self):
        """Metodo executado pelo cron de NFe. O metodo filtra
        os doc. eletrônicos elegíveis para envio. Caso o certificado
        esteja expirado ou a sua fatura nao esteja confirmada,
        o doc. eletronico não sera enviado.
        """
        domain = [
            ('state', '=', 'open'),
            ('model', '=', '001'),
            ('webservice_nfse', '=', 'nfse_ginfes'),
        ]

        nfes = self.env['invoice.electronic'].search(domain, limit=15)

        # Chama o metodo de envio dos doc. eletronico. Cada
        # tipo de Doc. eletronico tem seu proprio metodo de envio
        nfes.action_get_electronic_invoice_status()

        # Chamamos o cron por ultimo porque caso se o chamarmos primeiro
        # os RPS que acabaram de ser emitidos ja serao consultados. Como o
        # tempo de conversao pode demorar alguns segundos, poderia ocorrer
        # do RPS ainda nao ter sido convertido e desperdicarmos a requisicao
        super(InvoiceElectronic, self).cron_send_nfe()
