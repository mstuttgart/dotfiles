# © 2018 Danimar Ribeiro <danimaribeiro@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re
import base64
import pytz
import urllib3
import requests
import logging

from odoo import api, fields, models

from odoo.addons.br_nfse_goiania.models.const import TIPORPS, NATUREZA_OPERACAO, INC_CULTURAL

_logger = logging.getLogger(__name__)

try:
    import pytrustnfe.nfse.goiania
    import pytrustnfe.certificado
except ImportError:
    _logger.error('Cannot import pytrustnfe', exc_info=True)


STATE = {'edit': [('readonly', False)]}


class InvoiceElectronic(models.Model):
    _inherit = 'invoice.electronic'

    webservice_nfse = fields.Selection(selection_add=[
        ('nfse_goiania', 'Nota Fiscal Serviço (goiania)'),
    ])

    nfse_goiania_tipo_rps = fields.Selection(
        selection=TIPORPS,
        string='Tipo de RPS (goiania)',
    )

    nfse_goiania_natureza_operacao = fields.Selection(
        selection=NATUREZA_OPERACAO,
        string='Natureza da Operação (goiania)',
    )

    nfse_goiania_incentivador_cultural = fields.Selection(
        selection=INC_CULTURAL,
        string='Incentivador Cultural (goiania)',
    )

    @api.multi
    def _hook_validation(self):
        errors = super(InvoiceElectronic, self)._hook_validation()

        if self.model == '001' and self.webservice_nfse == 'nfse_goiania':

            if not self.company_id.inscr_mun:
                errors.append('Inscrição municipal obrigatória')

            if not self.company_id.cnae_main_id.code:
                errors.append('CNAE Principal da empresa obrigatório')

            if not self.codigo_tributacao_municipio:
                errors.append('Código de tributação do município obrigatório')

            for eletr in self.electronic_item_ids:

                prod = f"Produto: {eletr.product_id.default_code} - {eletr.product_id.name}"

                if eletr.tipo_produto == 'product':
                    errors.append(f'Esse documento permite apenas serviços - {prod}')

                if eletr.tipo_produto == 'service':

                    if not eletr.issqn_codigo:
                        errors.append(f'{prod} - Código de Serviço')

        return errors

    @api.multi
    def _prepare_electronic_invoice_values(self):
        res = super(InvoiceElectronic, self)._prepare_electronic_invoice_values()  # noqa

        if self.model != '001' or self.webservice_nfse != 'nfse_goiania':
            return res

        tz = pytz.timezone(self.env.user.partner_id.tz) or pytz.utc

        dt_emissao = pytz.utc.localize(self.data_emissao).astimezone(tz)
        dt_emissao = dt_emissao.strftime('%Y-%m-%dT%H:%M:%S')

        partner = self.commercial_partner_id
        city_tomador = partner.city_id

        tomador = {
            # 'tipo_cpfcnpj': 2 if partner.is_company else 1,
            'cnpj_cpf': re.sub('[^0-9]', '', partner.cnpj_cpf or ''),  # noqa
            'razao_social': partner.legal_name or partner.name,

            # 'cep': re.sub('[^0-9]', '', partner.zip),
            # 'telefone': re.sub('[^0-9]', '', partner.phone or ''),
            'inscricao_municipal': partner.inscr_mun or '',
            # 'email': self.partner_id.email or partner.email or '',
        }

        tomador['endereco'] = {
            'rua': partner.street or '',
            'numero': partner.number or '',
            'complemento': partner.street2 or '',
            'bairro': partner.district or 'Sem Bairro',
            # 'codigo_municipio': f'{city_tomador.state_id.ibge_code}{city_tomador.ibge_code}',
            'codigo_municipio': '2350000',
            'uf': partner.state_id.code,
        }

        city_prestador = self.company_id.partner_id.city_id

        prestador = {
            'cnpj_cpf': re.sub('[^0-9]', '', self.company_id.partner_id.cnpj_cpf or ''),  # noqa
            'inscricao_municipal': re.sub('[^0-9]', '', self.company_id.partner_id.inscr_mun or ''),  # noqa
            # 'cidade': '%s%s' % (city_prestador.state_id.ibge_code,
            #                     city_prestador.ibge_code),
            # 'cnae': re.sub('[^0-9]', '', self.company_id.cnae_main_id.code)
        }

        # itens_servico = []
        descricao = []
        # codigo_servico = ''

        for item in self.electronic_item_ids:

            descricao.append(item.name)

            # itens_servico.append({
            #     'descricao': item.name,
            #     'quantidade': str("%.2f" % item.quantidade),
            #     'valor_unitario': str("%.2f" % item.preco_unitario)
            # })

            # codigo_servico = item.issqn_codigo

        descricao = '\n'.join(descricao)

        servico = {
            'valor_servicos': f'{self.valor_final:0.2f}',
            'valor_pis': f'{abs(self.valor_retencao_pis):0.2f}',
            'valor_confins': f'{abs(self.valor_retencao_cofins):0.2f}',
            'valor_inss': f'{abs(self.valor_retencao_inss):0.2f}',
            'valor_csll': f'{abs(self.valor_retencao_csll):0.2f}',
            # 'aliquota': f'{self.electronic_item_ids[0].issqn_aliquota / 100}:0.4f',
            'codigo_tributacao_municipio': re.sub('[^0-9]', '', self.codigo_tributacao_municipio),
            'discriminacao': descricao,
            # 'codigo_municipio': f'{city_prestador.state_id.ibge_code}{city_prestador.ibge_code}',
            'codigo_municipio': '02530000',
        }

        rps = {
            # 'numero_lote': self.id,
            'numero': self.numero_rps,
            'serie': self.serie.code or '',
            'tipo': self.nfse_goiania_tipo_rps,
            'data_emissao': dt_emissao,
            # 'natureza_operacao': self.nfse_goiania_natureza_operacao,  # Tributada no municipio
            # 'optante_simples': '2' if self.company_id.fiscal_type == '3' else '1',  # 1 - Sim, 2 - Não
            # 'incentivador_cultural': self.nfse_goiania_incentivador_cultural,
            'status': '1',  # 1 - Normal
            # 'valor_servico': str("%.2f" % abs(self.valor_final)),
            # 'valor_deducao': '0',
            # 'valor_pis': str("%.2f" % abs(self.valor_retencao_pis)),
            # 'valor_cofins': str("%.2f" % abs(self.valor_retencao_cofins)),
            # 'valor_inss': str("%.2f" % abs(self.valor_retencao_inss)),
            # 'valor_ir': str("%.2f" % abs(self.valor_retencao_irrf)),
            # 'valor_csll': str("%.2f" % abs(self.valor_retencao_csll)),
            # 'iss_retido': '1' if self.valor_retencao_issqn > 0 else '2',
            # 'valor_iss':  str("%.2f" % abs(self.valor_issqn)),
            # 'valor_iss_retido': str("%.2f" % abs(self.valor_retencao_issqn)),
            # 'base_calculo': str("%.2f" % abs(self.valor_final)),
            # 'aliquota_issqn': str("%.4f" % (self.electronic_item_ids[0].issqn_aliquota / 100)),  # noqa
            # 'valor_liquido_nfse': str("%.2f" % self.valor_final),
            # 'cnae_servico': re.sub('[^0-9]', '', self.company_id.cnae_main_id.code),
            # 'codigo_servico': codigo_servico,
            # 'codigo_tributacao_municipio': re.sub('[^0-9]', '', self.codigo_tributacao_municipio),  # noqa
            # 'descricao': descricao,
            # 'codigo_municipio': prestador['cidade'],
            'servico': servico,
            'tomador': tomador,
            'prestador': prestador,
        }

        res.update(rps)
        res = pytrustnfe.utils.remove_especial_characters(res)
        return res

    @api.multi
    def action_send_electronic_invoice(self):
        """Realiza o envio de doc. eletronicos do NFSe Paulistana.
        O envio é realizado de forma assincrona. A
        """
        super(InvoiceElectronic, self).action_send_electronic_invoice()

        for rec in self:

            if rec.model == '001' and rec.webservice_nfse == 'nfse_goiania' and rec.state not in ('done', 'cancel'):

                rec.state = 'error'
                nfse_values = rec._prepare_electronic_invoice_values()

                cert = rec.company_id.with_context({'bin_size': False}).nfe_a1_file  # noqa
                cert_pfx = base64.decodestring(cert)

                certificado = pytrustnfe.certificado.Certificado(
                    cert_pfx, rec.company_id.nfe_a1_password)

                xml_enviar = pytrustnfe.nfse.goiania.xml_gerar_nfse(
                    certificado, rps=nfse_values)

                # salva xml de envio para referencia em caso de erro
                rec.xml_to_send = base64.encodestring(xml_enviar.encode('utf-8'))  # noqa
                rec.xml_to_send_name = f'nfse-envio-{rec.numero}.xml'

                try:

                    resposta = pytrustnfe.nfse.goiania.gerar_nfse(
                        certificado, xml=xml_enviar, ambiente=rec.ambiente)

                except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):

                    msg = """Erro de Timeout na requisição: Não foi possivel se conectar ao SEFAZ.
                    O SEFAZ pode estar offline ou sofrendo instabilidade em sua conexão.
                    Por favor, tente mais tarde."""

                    # Criamos um evento para sinalizar que a NFe esta com ERRO de timeout
                    self.env['invoice.electronic.event'].create({
                        'code': 'TIMEOUT',
                        'name': msg,
                        'invoice_electronic_id': rec.id,
                        'category': 'warning',
                    })

                    rec.write({
                        'codigo_retorno': 'TIMEOUT',
                        'mensagem_retorno': msg,
                        'state': 'draft',
                    })

                    continue

                retorno = resposta['object']

                vals = {}
                event_vals = {}

                # import ipdb; ipdb.set_trace()  # noqa


                if "ListaNfse" in dir(retorno):

                    inf_nfse = retorno.ListaNfse.CompNfse.Nfse.InfNfse

                    # o numero de nfse retornado excede o limite de tamanho do
                    # valor 'Integer', entao separamos esse numero em seu prefixo
                    # (o ano de emissao do RPS) e o numero da nota em si.
                    vals.update({
                        'state': 'done',
                        'codigo_retorno': '100',
                        'mensagem_retorno': 'NFSe emitida com sucesso',
                        'verify_code': inf_nfse.CodigoVerificacao.text,  # noqa
                        'numero_prefixo': inf_nfse.Numero.text[:4],
                        'numero': inf_nfse.Numero.text[4:],
                        'data_autorizacao': fields.Date.from_string(inf_nfse.DataEmissao.text[:10]),
                        # 'lote_code': retorno.NumeroLote.text,
                        'recibo_nfe': retorno.Protocolo.text,
                    })

                    event_vals.update({
                        'category': 'info',
                        'code': '100',
                        'name': 'NFSe emitida com sucesso',
                        'invoice_electronic_id': rec.id,
                    })

                else:
                    msg = None

                    if "ListaMensagemRetorno" in dir(retorno):
                        msg = retorno.ListaMensagemRetorno.MensagemRetorno

                        # RPS já emitido na prefeitura
                        if msg.Codigo == 'E10':
                            category = 'warning'
                            state = 'open'
                        else:
                            state = 'error'
                            category = 'error'

                        event_vals.update({
                            'code': msg.Codigo,
                            'name': msg.Mensagem,
                            'invoice_electronic_id': rec.id,
                            'category': category,
                        })

                        vals.update({
                            'state': state,
                            'codigo_retorno': msg.Codigo or '',
                            'mensagem_retorno': msg.Mensagem or '',
                            # 'lote_code': retorno.NumeroLote.text,
                            # 'recibo_nfe': retorno.Protocolo.text,
                        })

                rec.write(vals)
                self.env['invoice.electronic.event'].create(event_vals)

                if rec.state == 'done':
                    rec.invoice_id.write({
                        'internal_number': rec.numero,
                        'date_invoice': fields.Date.from_string(rec.data_autorizacao),  # noqa
                    })

                rec._create_attachment('nfse-envio', rec, resposta['sent_xml'])

                rec._create_attachment('nfse-ret', rec, resposta['received_xml'])

    def action_get_electronic_invoice_status(self):
        """Realiza consulta do status do RPS dos doc. eletronicos
        já enviados para a prefeitura. Se o RPS foi enviado em ambiente de homologacao,
        o lote nao e gerado na prefeitura. Sendo assim, a consulta ira retorno
        erro de 'Lote nao encontrado'
        """
        super(InvoiceElectronic, self).action_get_electronic_invoice_status()

        for rec in self:

            if rec.model == '001' and rec.webservice_nfse == 'nfse_goiania' and rec.state in ['open', 'error']:

                # partner_prestador = rec.company_id.partner_id
                cert = rec.company_id.with_context({'bin_size': False}).nfe_a1_file  # noqa
                cert_pfx = base64.decodestring(cert)

                certificado = pytrustnfe.certificado.Certificado(
                    cert_pfx, rec.company_id.nfe_a1_password)

                nfse_values = {
                    'cnpj': re.sub('[^0-9]', '', rec.company_id.partner_id.cnpj_cpf or ''),  # noqa
                    'inscricao_municipal': re.sub('[^0-9]', '', rec.company_id.partner_id.inscr_mun or ''),  # noqa
                    'numero': rec.numero_rps,
                    'serie': rec.serie.code or '',
                    'tipo_rps': rec.nfse_goiania_tipo_rps,
                }

                resposta = pytrustnfe.nfse.goiania.consultar_nfse_por_rps(
                    certificado, nfse=nfse_values, ambiente=rec.ambiente)

                retorno = resposta['object']

                if "CompNfse" in dir(retorno):

                    inf_nfse = retorno.CompNfse.Nfse.InfNfse

                    # o numero de nfse retornado excede o limite de tamanho do
                    # valor 'Integer', entao separamos esse numero em seu prefixo
                    # (o ano de emissao do RPS) e o numero da nota em si.
                    rec.write({
                        'state': 'done',
                        'codigo_retorno': '100',
                        'mensagem_retorno': 'NFSe emitida com sucesso',
                        'verify_code': inf_nfse.CodigoVerificacao.text,  # noqa
                        'numero_prefixo': inf_nfse.Numero.text[:4],
                        'numero': inf_nfse.Numero.text[4:],
                        'data_autorizacao': fields.Date.from_string(inf_nfse.DataEmissao.text[:10]),
                    })

                    self.env['invoice.electronic.event'].create({
                        'category': 'info',
                        'code': '100',
                        'name': 'NFSe emitida com sucesso',
                        'invoice_electronic_id': rec.id,
                    })

                    rec.invoice_id.write({
                        'internal_number': rec.numero,
                        'date_invoice': rec.data_autorizacao,
                    })

                    self._create_attachment('consul-nfe-envio', rec, str(resposta['sent_xml']))  # noqa
                    self._create_attachment('consulnfe-ret', rec, str(resposta['received_xml']))  # noqa

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

        res = super(InvoiceElectronic, self).action_cancel_document(justificativa=justificativa, context=context)  # noqa

        if self.model == '001' and self.webservice_nfse == 'nfse_goiania' and self.state in ['done']:

            cert = self.company_id.with_context({'bin_size': False}).nfe_a1_file  # noqa

            cert_pfx = base64.decodestring(cert)

            certificado = pytrustnfe.certificado.Certificado(
                cert_pfx, self.company_id.nfe_a1_password)

            company = self.company_id
            city_prestador = self.company_id.partner_id.city_id

            canc = {
                'cnpj_prestador': re.sub('[^0-9]', '', company.cnpj_cpf),
                'inscricao_municipal': re.sub('[^0-9]', '', company.inscr_mun),
                'cidade': '%s%s' % (city_prestador.state_id.ibge_code,
                                    city_prestador.ibge_code),
                'numero_nfse': str(self.numero_prefixo or '') + str(self.numero or '').zfill(11),
                'codigo_cancelamento': '1',  # Erro na emissão
            }

            try:

                cancelar_nfse = pytrustnfe.nfse.goiania.cancelar_nfse(
                    certificado, cancelamento=canc, ambiente=self.ambiente)

            except (urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):

                msg = """Erro de Timeout na requisição: Não foi possivel se conectar ao SEFAZ.
                O SEFAZ pode estar offline ou sofrendo instabilidade em sua conexão.
                Por favor, tente mais tarde."""

                # Criamos um evento para sinalizar que a NFe esta com ERRO de timeout
                self.env['invoice.electronic.event'].create({
                    'code': 'TIMEOUT',
                    'name': msg,
                    'invoice_electronic_id': self.id,
                    'category': 'warning',
                })

                return res

            retorno = cancelar_nfse['object']

            vals = {}
            event_vals = {}

            if "RetCancelamento" in dir(retorno):

                vals.update({
                    'state': 'cancel',
                    'codigo_retorno': '100',
                    'mensagem_retorno': 'Nota Fiscal de Serviço Cancelada'
                })

                event_vals.update({
                    'code': vals['codigo_retorno'],
                    'name': vals['mensagem_retorno'],
                    'category': 'info',
                    'invoice_electronic_id': self.id,
                })

            else:

                msg = retorno.ListaMensagemRetorno.MensagemRetorno

                event_vals.update({
                    'code': msg.Codigo,
                    'name': msg.Mensagem,
                    'invoice_electronic_id': self.id,
                    'category': 'error',
                })

                vals.update({
                    'state': 'error',
                    'codigo_retorno': msg.Codigo,
                    'mensagem_retorno': msg.Mensagem,
                })

                # E79 - Nota já está cancelada na prefeitura
                if msg.Codigo == 'E79':

                    event_vals.update({
                        'category': 'warning',
                    })

                    # Criamos um evento adicional para deixar registrado que a NFSe
                    # ja estava cancelada na prefeitura
                    self.env['invoice.electronic.event'].create(event_vals)

                    # Atualizamos os dados do edoc para nfse cancelada
                    event_vals.update({
                        'code': '100',
                        'name': 'Nota Fiscal de Serviço Cancelada',
                        'invoice_electronic_id': self.id,
                        'category': 'info',
                    })

                    vals.update({
                        'state': 'cancel',
                        'codigo_retorno': '100',
                        'mensagem_retorno': 'Nota Fiscal de Serviço Cancelada'
                    })

            self.write(vals)
            self.env['invoice.electronic.event'].create(event_vals)

            self._create_attachment('canc', self, cancelar_nfse['sent_xml'])
            self._create_attachment('canc-ret', self, cancelar_nfse['received_xml'])  # noqa

        return res

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
            ('webservice_nfse', '=', 'nfse_goiania'),
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
