import json
import re
import base64
import pytz
import requests

from odoo import api, fields, models
from odoo.exceptions import UserError
# from odoo.addons.br_account_einvoice_tecnospeed.models.const import URL_PRODUCAO, URL_SANDBOX
from odoo.addons.br_nfse_tecnospeed.models.const import NATUREZA_OPERACAO

STATE = {'edit': [('readonly', False)]}


class InvoiceElectronic(models.Model):
    _inherit = 'invoice.electronic'

    webservice_nfse = fields.Selection(selection_add=[
        ('nfse_tecnospeed', 'Nota Fiscal Serviço (Tecnospeed)'),
    ])

    nfse_tecnospeed_natureza_operacao = fields.Selection(
        selection=NATUREZA_OPERACAO,
        string='Natureza da Operação (tecnospeed)',
    )

    tecnospeed_nfse_pdf = fields.Binary(string='URL PDF')
    tecnospeed_nfse_pdf_name = fields.Char(string='NFSe PDF Filename')

    @api.multi
    def _hook_validation(self):
        """Realiza validacao de campos criticos para emissao da NFSe.

        Returns:
            list: Lista de erros que detectados
        """

        errors = super(InvoiceElectronic, self)._hook_validation()

        if self.model == '001' and self.nfe_engine == 'tecnospeed':

            # if self.company_id.tecnospeed_sandbox_active and not self.company_id.tecnospeed_certificado_id_sandbox:
            #     errors.append('Token para ambiente Sandbox obrigatório')

            # if not self.company_id.tecnospeed_sandbox_active and not self.company_id.tecnospeed_certificado_id_producao:
            #     errors.append('Token para ambiente Produção/Homologação obrigatório')

            issqn_codigo = ''

            if not self.company_id.inscr_mun:
                errors.append('Inscrição municipal obrigatória')

            if not self.codigo_tributacao_municipio:
                errors.append('Código de tributação do município obrigatório')

            for eletr in self.electronic_item_ids:

                prod = f"Produto: {eletr.product_id.default_code} - {eletr.product_id.name}"

                if eletr.tipo_produto == 'product':
                    errors.append(f'Esse documento permite apenas serviços - {prod}')

                if eletr.tipo_produto == 'service':

                    if not eletr.issqn_codigo:
                        errors.append(f'{prod} - Código de Serviço')

                    if not issqn_codigo:
                        issqn_codigo = eletr.issqn_codigo

                    if issqn_codigo != eletr.issqn_codigo:
                        errors.append(f'{prod} - Apenas itens com o mesmo código de serviço podem ser enviados')

        return errors

    @api.multi
    def _prepare_electronic_invoice_values(self):
        """Monta dict com valores para montagem do XML para envio
        da NFSe

        Returns:
            dict: dicionario com os campos da NFSE
        """

        res = super(InvoiceElectronic, self)._prepare_electronic_invoice_values()  # noqa

        if self.model == '001' and self.nfe_engine == 'tecnospeed':

            # Prestador
            # ------------------------------------------------------------

            partner_prestador = self.company_id.partner_id

            # A numeracao do tipo fiscal da empresa nao bate com a numeracao
            # usada na tecnospeed. Sendo assim tivemos que realizar o mapeamento abaixo
            if self.company_id.fiscal_type in ('1', '2', '4'):
                regime_tributario = self.company_id.fiscal_type

            elif self.company_id.fiscal_type == '5':
                regime_tributario = '3'

            else:
                regime_tributario = '0'

            prestador = {
                'cpfCnpj': re.sub('[^0-9]', '', partner_prestador.cnpj_cpf or ''),
                # 'codigoEstrangeiro': '',
                'endereco': {
                    'bairro': partner_prestador.district,
                    'cep': re.sub('[^0-9]', '', partner_prestador.zip or '') or '',
                    'codigoCidade': f'{partner_prestador.state_id.ibge_code}{partner_prestador.city_id.ibge_code}' or '',
                    # 'codigoCidade': '025300'.zfill(7),
                    'estado': partner_prestador.state_id.code,
                    'logradouro': partner_prestador.street,
                    'numero': partner_prestador.number or '',
                    'tipoLogradouro': 'Avenida',
                    'codigoPais': partner_prestador.country_id.ibge_code,
                    'complemento': partner_prestador.street2 or '',
                    'descricaoCidade': partner_prestador.city_id.name,
                    # 'descricaoCidade': 'Goiania',
                    'descricaoPais': 'Brasil',
                    'tipoBairro': 'Setor',
                },
                # 'email': partner_prestador.email or '',
                # 'incentivadorCultural': self.company_id.tecnospeed_incentivador_cultural,
                # 'incentivoFiscal': self.company_id.tecnospeed_incentivo_fiscal,
                # 'inscricaoEstadual': re.sub('[^0-9]', '', partner_prestador.inscr_est or ''),
                'inscricaoMunicipal': re.sub('[^0-9]', '', partner_prestador.inscr_mun or ''),
                # 'nomeFantasia': partner_prestador.name,
                'razaoSocial': partner_prestador.legal_name or '',
                'regimeTributario': int(regime_tributario),
                'regimeTributarioEspecial': int(self.company_id.tecnospeed_regime_tributacao),
                'simplesNacional': True if self.company_id.fiscal_type in ('1', '2') else False,
                'telefone': {
                    # 'numero': re.sub('[^0-9]', '', partner_prestador.phone or ''),
                    'numero': "5555555555",
                    # 'ddd': '85',
                },
                # 'codigoDistrito': '',
            }

            # tomador
            # ---------------------------------------------------------------------------

            partner = self.commercial_partner_id

            tomador = {
                'cpfCnpj': re.sub('[^0-9]', '', partner.cnpj_cpf or ''),
                'razaoSocial': partner.legal_name or '',
                'endereco': {
                    'bairro': partner.district or '',
                    'cep': re.sub('[^0-9]', '', partner.zip or '') or '',
                    'codigoCidade': f'{partner.state_id.ibge_code}{partner.city_id.ibge_code}',
                    # 'codigoCidade': '023500'.zfill(7),
                    'estado': partner.state_id.code,
                    'logradouro': partner.street,
                    'numero': partner.number or '',
                    'tipoLogradouro': 'Avenida',
                    'codigoPais': partner.country_id.ibge_code,
                    'complemento': partner.street2 or '',
                    'descricaoCidade': partner.city_id.name,
                    'descricaoPais': partner.country_id.name,
                    # 'tipoBairro': '',
                },
                # 'email': partner.email or '',
                # 'inscricaoEstadual': re.sub('[^0-9]', '', partner.inscr_est or ''),
                # 'inscricaoMunicipal': re.sub('[^0-9]', '', partner.inscr_mun or ''),
                # 'nomeFantasia': partner.name,
                # 'orgaoPublico': False,
                # 'telefone': {
                #     'numero': re.sub('[^0-9]', '', partner.phone or ''),
                # },
                # 'codigoEstrangeiro': '',
            }

            # servico
            # ------------------------------------------------

            servicos = []
            descricao = []

            for item in self.electronic_item_ids:

                descricao.append(item.name)

                servicos.append({
                    'codigo': item.issqn_codigo,
                    # 'discriminacao': item.name,
                    'discriminacao': "Servico Teste",
                    # 'codigoTributacao': re.sub('[^0-9]', '', self.codigo_tributacao_municipio),
                    # 'codigoTributacao': re.sub('[^0-9]', '', '702040000'),
                    # 'codigoTributacao': '',
                    # 'cnae': re.sub('[^0-9]', '', self.company_id.cnae_main_id.code),
                    # # 'codigoCidadeIncidencia': '',
                    # # 'descricaoCidadeIncidencia': '',
                    # 'unidade': item.uom_id.name or '',
                    # 'quantidade': item.quantidade,
                    'iss': {
                        # 'tipoTributacao': '',
                        # 'exigibilidade': '',
                        # 'retido': False if item.issqn_valor_retencao > 0 else True,
                        'aliquota': item.issqn_aliquota,
                        # 'aliquota': str("%.4f" % (item.issqn_aliquota / 100)),
                        # 'valor': abs(item.issqn_valor),
                        # 'valorRetido': abs(item.issqn_valor_retencao),
                        # 'processoSuspensao': '',
                    },
                    # 'obra': {},
                    'valor': {
                        'servico': self.valor_final,
                        # 'servico': str("%.2f" % abs(item.valor_bruto)),
                        # 'baseCalculo': item.valor_bruto,
                        # 'deducoes': 0,
                        # 'descontoCondicionado': 0,
                        # 'descontoIncondicionado': 0,
                        # 'liquido': item.valor_liquido,
                        # 'unitario': item.preco_unitario,
                    },
                    # 'deducao': {},
                    'retencao': {
                        # 'pis': {
                        #     'baseCalculo': item.pis_base_calculo,
                        #     'aliquota': item.pis_aliquota,
                        #     'valor': item.pis_valor_retencao,
                        # },
                        # 'cofins': {
                        #     'baseCalculo': item.cofins_base_calculo,
                        #     'aliquota': item.cofins_aliquota,
                        #     'valor': item.cofins_valor_retencao,
                        # },
                        # 'csll': {
                        #     'aliquota': item.csll_aliquota,
                        #     'valor': item.csll_valor_retencao,
                        # },
                        # 'inss': {
                        #     'aliquota': item.inss_aliquota,
                        #     'valor': item.inss_valor_retencao,
                        # },
                        # 'irrf': {
                        #     'aliquota': item.irrf_aliquota,
                        #     'valor': item.irrf_valor_retencao,
                        # },
                        # 'cpp': {
                        #     'aliquota': 0,
                        #     'valor': 0,
                        # },
                        # 'outrasRetencoes': 0,
                    },
                    # 'tributavel': False,
                    # 'ibpt': {
                    #     'detalhado': {
                    #         'aliquota': {
                    #             'municipal': self.fiscal_position_id.service_type_id.municipal_imposto / 100,
                    #             'estadual': self.fiscal_position_id.service_type_id.estadual_imposto / 100,
                    #             'federal': self.fiscal_position_id.service_type_id.federal_nacional / 100,
                    #         },
                    #     },
                    # },
                    # 'responsavelRetencao': '',
                })

            tz = pytz.timezone(self.env.user.partner_id.tz) or pytz.utc
            dt_emissao = pytz.utc.localize(self.data_emissao).astimezone(tz)

            rps = {
                # 'competencia': dt_emissao.strftime('%Y-%m-%d'),
                'dataEmissao': dt_emissao.strftime('%Y-%m-%dT%H:%M:%S'),
                # 'dataVencimento': '',
                'serie': self.serie.code or '',
                'numero': self.numero_rps,
            }

            nfse_vals = {
                'idIntegracao': str(self.id),
                'prestador': prestador,
                'tomador': tomador,
                'servico': servicos,
                # 'deducao': [],
                # 'cargaTributaria': {},
                # 'cidadePrestacao': {},
                # 'descricao': '\n'.join(descricao),
                'enviarEmail': False,
                # 'idNotaSubstituida': '',
                # 'impressao': {},
                'camposPrefeitura': {
                    'codigoCidade': '0025300',
                    # 'tomador': {
                    #     'endereco': {
                    #         'CodigoMunicipio': '0023500',
                    #     }
                    # },
                },
                # 'informacoesComplementares': '',
                # 'intermediario': {},
                # 'naturezaTributacao': '',
                'rps': rps,
                # 'parcelas': [],
                # 'camposExtras': {},
            }

            res.update(nfse_vals)

        return res

    @api.multi
    def action_send_electronic_invoice(self):
        """Realiza o envio de doc. eletronicos do NFSe Paulistana.
        O envio é realizado de forma assincrona. A
        """

        super(InvoiceElectronic, self).action_send_electronic_invoice()

        for rec in self:

            if rec.model != '001' or rec.nfe_engine != 'tecnospeed' or rec.state != 'draft':
                continue

            values = rec._prepare_electronic_invoice_values()

            request_vals = rec.company_id.get_tecnospeed_request_vals(subdomain='nfse')

            payload = json.dumps([values])

            # import ipdb; ipdb.set_trace()  # noqa


            # payload = payload.replace('ç', 'c')
            # payload = payload.replace('ã', 'a')
            # payload = payload.replace('â', 'a')
            # payload = payload.replace('õ', 'o')
            # payload = payload.replace('á', 'a')
            # payload = payload.replace('à', 'a')
            # payload = payload.replace('é', 'e')
            # payload = payload.replace('è', 'e')
            # payload = payload.replace('í', 'i')
            # payload = payload.replace('ì', 'i')
            # payload = payload.replace('ó', 'o')
            # payload = payload.replace('ò', 'o')
            # payload = payload.replace('ù', 'u')
            # payload = payload.replace('ú', 'u')

            # payload = payload.replace('Á', 'A')
            # payload = payload.replace('À', 'A')
            # payload = payload.replace('Â', 'A')

            # payload = payload.replace('Ú', 'U')
            # payload = payload.replace('Ù', 'u')

            # payload = payload.replace('É', 'e')
            # payload = payload.replace('È', 'e')

            # payload = payload.replace('Í', 'I')
            # payload = payload.replace('Ì', 'I')

            # payload = payload.replace('Ó', 'O')
            # payload = payload.replace('Ò', 'O')

            # import ipdb; ipdb.set_trace()  # noqa

            # char_list = {
            #     '<': ' ',
            #     '>': ' ',
            #     '&': 'e',
            #     '"': ' ',
            #     '\'': ' ',
            #     'ª': 'a',
            #     'º': 'o',
            #     '´': ' ',
            #     '²': '2',
            #     '³': '3',
            #     '¹': '1',
            #     '§': ' ',
            # }

            # for ch in char_list:


            # salva anexo do json enviado
            self._create_attachment(
                'nfse-envio', rec, payload, extension='json',
            )

            try:



                response = requests.request(
                    'POST',
                    url=request_vals['url'],
                    headers=request_vals['headers'],
                    data=payload,
                    timeout=5,
                )

                # import ipdb; ipdb.set_trace()  # noqa


            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):

                msg = """Erro de conexão/timeout: Não foi possivel se conectar ao PlugNotas.
                O serviço PlugNotas offline ou sofrendo instabilidade em sua conexão.
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

            # salva anexo do json recebido
            self._create_attachment(
                'nfse-envio-ret', rec, response.text, extension='json',
            )

            res = json.loads(response.text)

            vals = {}
            vals_event = {
                'invoice_electronic_id': rec.id,
            }

            # o codigo 409 representa conflito.
            # Normalmente quando ja existe uma nfse com os mesmos dados
            if response.status_code == 409:

                vals.update({
                    'state': 'error',
                    'codigo_retorno': str(response.status_code),
                    'mensagem_retorno': f"{res['error']['message']}",
                })

                vals_event.update({
                    'code': str(response.status_code),
                    'name': f"{res['error']['message']}",
                    'category': 'error',
                })

            # o codigo 200 representa sucesso
            elif response.status_code != 200:

                # import ipdb; ipdb.set_trace()  # noqa

                if 'error' not in res:
                    res = {
                        'error': res
                    }


                vals.update({
                    'state': 'error',
                    'codigo_retorno': str(response.status_code),
                    'mensagem_retorno': f"{res['error']['message']}",
                })

                vals_event.update({
                    'code': str(response.status_code),
                    'name': f"{res['error']['message']}: {res['error']['data']}",
                    'category': 'error',
                })

            else:

                vals.update({
                    'tecnospeed_id_nota': res['documents'][0]['id'],
                    'state': 'open',
                    'codigo_retorno': '200',
                    'mensagem_retorno': res['message'],
                    'recibo_nfe': res['protocol'],
                })

                vals_event.update({
                    'code': str(response.status_code),
                    'name': res['message'],
                    'category': 'info',
                })

            rec.write(vals)
            self.env['invoice.electronic.event'].create(vals_event)

    def action_get_electronic_invoice_status(self):
        """Realiza consulta do status do RPS dos doc. eletronicos
        na prefeitura.
        """
        super(InvoiceElectronic, self).action_get_electronic_invoice_status()

        for rec in self:

            if rec.model != '001' or not rec.recibo_nfe or rec.nfe_engine != 'tecnospeed':
                continue

            if rec.state in ['open', 'error']:

                request_vals = rec.company_id.get_tecnospeed_request_vals(
                    subdomain=f'nfse/consultar/{rec.tecnospeed_id_nota}')

                try:

                    response = requests.request(
                        'GET',
                        url=request_vals['url'],
                        headers=request_vals['headers'],
                        timeout=5,
                    )

                except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):

                    msg = """Erro de conexão/timeout: Não foi possivel se conectar ao PlugNotas.
                    O serviço PlugNotas offline ou sofrendo instabilidade em sua conexão.
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

                res = json.loads(response.text)[0]

                # o codigo 200 representa sucesso
                if response.status_code != 200:

                    rec.write({
                        'state': 'error',
                        'codigo_retorno': str(response.status_code),
                        'mensagem_retorno': res['error']['message'],

                    })

                    self.env['invoice.electronic.event'].create({
                        'code': str(response.status_code),
                        'name': res['error']['message'],
                        'category': 'error',
                    })

                else:

                    vals = {}
                    vals_event = {
                        'invoice_electronic_id': rec.id,
                    }

                    if res['situacao'] == 'REJEITADO':

                        vals.update({
                            'state': 'error',
                            'codigo_retorno': 'ERROR',
                            'mensagem_retorno': res['mensagem'],
                        })

                        vals_event.update({
                            'code': 'ERROR',
                            'name': res['mensagem'],
                            'category': 'error',
                        })

                    elif res['situacao'] == 'CONCLUIDO':

                        vals.update({
                            'state': 'done',
                            'codigo_retorno': '100',
                            'mensagem_retorno': res['mensagem'],
                            'numero': res['numeroNfse'],
                            'verify_code': res['codigoVerificacao'],
                            'data_autorizacao': res['autorizacao'],
                            'tecnospeed_url_xml': res['xml'],
                            'tecnospeed_url_pdf': res['pdf'],
                        })

                        vals_event.update({
                            'code': '100',
                            'name': res['mensagem'],
                            'category': 'info',
                        })

                    elif res['situacao'] == 'CANCELADO':

                        vals.update({
                            'state': 'cancel',
                            'codigo_retorno': '100',
                            'mensagem_retorno': res['mensagem'],
                        })

                        date = res['cancelamento']
                        date = f'{date[6:10]}-{date[3:5]}-{date[0:2]}'
                        vals['cancel_date'] = fields.Date.to_date(date)

                        vals_event.update({
                            'code': '100',
                            'name': res['mensagem'],
                            'category': 'info',
                        })

                    elif res['situacao'] == 'PROCESSANDO':

                        vals.update({
                            'codigo_retorno': '200',
                            'mensagem_retorno': 'Nota(as) em processamento',
                        })

                        vals_event.update({
                            'code': '200',
                            'name': 'Nota(as) em processamento',
                            'category': 'info',
                        })

                    rec.write(vals)
                    self.env['invoice.electronic.event'].create(vals_event)

                    # Para evitar a criacao de varios arquivos anexos
                    if res['situacao'] !=  'PROCESSANDO':
                        # cria anexo do json retornado
                        self._create_attachment('cons-nfe-ret', rec, response.text, extension='json')  # noqa

                    if rec.state == 'done':

                        rec.invoice_id.write({
                            'internal_number': rec.numero,
                            'date_invoice': rec.data_autorizacao,
                        })

                        try:

                            # Realizamos o GET do XML da NFSe (concluido ou cancelado)
                            request_vals = rec.company_id.get_tecnospeed_request_vals(subdomain=f'nfse/xml/{rec.tecnospeed_id_nota}')  # noqa

                            response = requests.request(
                                'GET',
                                url=request_vals['url'],
                                headers=request_vals['headers'],
                                timeout=5,
                            )

                            if response.status_code == 200:
                                # salva xml da NFSe no anexo
                                self._create_attachment(
                                    'nfse-xml', rec, response.text, extension='xml')

                            # Realizamos o GET para o PDF do nfse
                            request_vals = rec.company_id.get_tecnospeed_request_vals(subdomain=f'nfse/pdf/{rec.tecnospeed_id_nota}')  # noqa

                            response = requests.request(
                                'GET',
                                url=request_vals['url'],
                                headers=request_vals['headers'],
                                timeout=5,
                            )

                            if response.status_code == 200:
                                # salva PDF na NFSe
                                rec.tecnospeed_nfse_pdf = base64.b64encode(response.content)  # noqa
                                rec.tecnospeed_nfse_pdf_name = f'{self.numero} - NFSe - {self.partner_id.name}.pdf'

                        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):

                            msg = """Erro de conexão/timeout: Não foi possivel se conectar ao PlugNotas.
                            O serviço PlugNotas offline ou sofrendo instabilidade em sua conexão.
                            Por favor, tente mais tarde."""

                            # Criamos um evento para sinalizar que a NFe esta com ERRO de timeout
                            self.env['invoice.electronic.event'].create({
                                'code': 'TIMEOUT (pdf/xml GET)',
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

    @api.multi
    def action_cancel_document(self, context=None, justificativa=None):
        """Realiza cancelamento de uma NFe. O envio de cancelamento é assincrono. Sendo assim,
        apos o pedido de confirmação, o deve-se consultar o status do nfe na API da Tecnospeed.

        Args:
            context (dict, optional): Contexto com variaveis usados no metodo. Defaults to None.
            justificativa (str, optional): Justificativa para cancelamento da NFe. Defaults to None.

        Returns:
            bool: True, se a gravacao do metodo ocorreu de forma correta. False, caso contrario.
        """

        res = super(InvoiceElectronic, self).action_cancel_document(context=context, justificativa=justificativa)  # noqa

        if self.model != '001' or self.nfe_engine != 'tecnospeed' or self.state != 'done':
            return res

        request_vals = self.company_id.get_tecnospeed_request_vals(subdomain=f'nfse/cancelar/{self.tecnospeed_id_nota}')  # noqa

        try:

            response = requests.request(
                'POST',
                url=request_vals['url'],
                headers=request_vals['headers'],
                timeout=5,
            )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):

            msg = """Erro de conexão/timeout: Não foi possivel se conectar ao PlugNotas.
            O serviço PlugNotas offline ou sofrendo instabilidade em sua conexão.
            Por favor, tente mais tarde."""

            # Criamos um evento para sinalizar que a NFe esta com ERRO de timeout
            self.env['invoice.electronic.event'].create({
                'code': 'TIMEOUT',
                'name': msg,
                'invoice_electronic_id': self.id,
                'category': 'warning',
            })

            self.write({
                'codigo_retorno': 'TIMEOUT',
                'mensagem_retorno': msg,
                'state': 'draft',
            })

            return

        response_json = json.loads(response.text)

        vals = {}
        vals_event = {
            'invoice_electronic_id': self.id,
        }

        # o codigo 200 representa sucesso
        if response.status_code != 200:

            if 'message' in response_json['error']:
                message = response_json['error']['message']
            else:
                message = response_json['message']

            vals.update({
                'codigo_retorno': str(response.status_code),
                'mensagem_retorno': message,

            })

            vals_event.update({
                'code': str(response.status_code),
                'name': message,
                'category': 'error',
            })

        else:

            vals.update({
                'state': 'open',
                'codigo_retorno': str(response.status_code),
                'mensagem_retorno': response_json['message'],
                'recibo_nfe': response_json['data']['protocol'],
            })

            vals_event.update({
                'code': str(response.status_code),
                'name': response_json['message'],
                'category': 'info',
            })

        self.write(vals)
        self.env['invoice.electronic.event'].create(vals_event)

        return res

    @api.multi
    def action_print_einvoice_report(self):

        res = super(InvoiceElectronic, self).action_print_einvoice_report()

        if self.model == '001' and self.nfe_engine != 'tecnospeed' and self.state in ['done', 'cancel'] and self.tecnospeed_nfse_pdf:  # noqa

            base_url = self.env['ir.config_parameter'].get_param(
                'web.base.url')

            file_url = f"{base_url}web/content?model=invoice.electronic&field=tecnospeed_nfse_pdf&filename_field=tecnospeed_nfse_pdf_name&id={self.id}"  # noqa

            res = {
                'type': 'ir.actions.act_url',
                'url': file_url,
                'target': 'new'
            }

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
            ('nfe_engine', '=', 'tecnospeed'),
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
