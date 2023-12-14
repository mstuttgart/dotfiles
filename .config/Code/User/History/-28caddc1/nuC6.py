import base64
import json
import urllib
import re

import requests

from odoo import fields, models
from odoo.addons.br_account_einvoice_tecnospeed.models.const import URL_PRODUCAO, URL_SANDBOX, SEND_NFE_API, TRIBUTACAO
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    nfe_engine = fields.Selection(
        selection=SEND_NFE_API,
        default='pytrustnfe',
        string='Engine para envio de NFe'
    )

    nfse_engine = fields.Selection(
        selection=SEND_NFE_API,
        default='pytrustnfe',
        string='Engine para envio de NFSe'
    )

    tecnospeed_regime_tributacao = fields.Selection(
        selection=TRIBUTACAO,
        default='1',
        string='Regime de Tributação (Tecnospeed)',
        help='Código de identificação do regime especial de tributação',
    )

    tecnospeed_incentivador_cultural = fields.Boolean(
        string='Incentivador Cultural (Tecnospeed)',
    )

    tecnospeed_incentivo_fiscal = fields.Boolean(
        string='Incentivo Fiscal (Tecnospeed)',
    )

    tecnospeed_sandbox_active = fields.Boolean(
        string='Sandbox active (developer)',
        help="""Ativa modo sandbox para desenvolvimento. Com esse modo ativado,
        as resposta do webservice sao padronizadas pela Tecnospeed"""
    )

    tecnospeed_certificado_id_sandbox = fields.Char(
        string='Certificado ID (sandbox)',
    )

    tecnospeed_certificado_id_producao = fields.Char(
        string='Certificado ID (producao)',
    )

    def get_tecnospeed_request_vals(self, subdomain, content_type='application/json;charset=utf-8'):
        """Realiza a montagem dos header e da url baseado no ambiente
        seleciona (sandbox ou produção/homologação)

        Args:
            subdomain (str): endpoint a ser consumido pela API
            content_type (str, optional): Content-Type a ser utilizado na requisição. Defaults to 'application/json'.

        Returns:
            dict: dict contendo a URL completa e o headers para requisição
        """

        get_param = self.env['ir.config_parameter'].sudo().get_param

        if self.tecnospeed_sandbox_active:

            url = f'{URL_SANDBOX}'
            token = get_param(
                'br_account_einvoice_tecnospeed.tecnospeed_token_sandbox',
            )

        else:

            url = f'{URL_PRODUCAO}'
            token = get_param(
                'br_account_einvoice_tecnospeed.tecnospeed_token_producao',
            )

            if not token:
                raise UserError('TOKEN de usuário Tecnospeed ausente')

        headers = {
            'x-api-key': token,
        }

        if content_type:
            headers['Content-Type'] = content_type

        return {
            'url': urllib.parse.urljoin(url, subdomain),
            'headers': headers,
        }

    def action_post_tecnospeed_certificado(self):
        """Realiza o POST e PUT para obter/atualizar
        o ID do certificado no PlugNotas (tecnospeed). O ambiente
        selecionado depende se o ambiente de 'sandbox' esta ou não ativo.

        Raises:
            UserError: Token de usuario ausento para ambiente de produção/homologação
            UserError: Erro de conexão com o ambiente do PlugNotas
            UserError: Erro na montagem dos parametros da requisição
            UserError: Erro retornado pelo PlugNotas, como ID de certificado inexistente, por exemplo.
        """

        # ambiente de desenvolvimento sandbox
        if self.tecnospeed_sandbox_active:

            # atualiza ID certificado
            if self.tecnospeed_certificado_id_sandbox:
                action = 'PUT'
                request_vals = self.get_tecnospeed_request_vals(subdomain=f'certificado/{self.tecnospeed_certificado_id_sandbox}', content_type=None)

            # cadastra certificado e obtem seu ID
            else:
                action = 'POST'
                request_vals = self.get_tecnospeed_request_vals(
                    subdomain='certificado', content_type=None)

        else:

            # atualiza ID certificado
            if self.tecnospeed_certificado_id_producao:
                action = 'PUT'
                request_vals = self.get_tecnospeed_request_vals(subdomain=f'certificado/{self.tecnospeed_certificado_id_producao}', content_type=None)

            # cadastra certificado e obtem seu ID
            else:
                action = 'POST'
                request_vals = self.get_tecnospeed_request_vals(subdomain='certificado', content_type=None)

        files = [
            ('arquivo', ('cert.pfx', base64.b64decode(self.nfe_a1_file), 'application/octet-stream'))
        ]

        payload = {
            'senha': self.nfe_a1_password,
            'arquivo': 'cert.pfx',
        }

        try:

            response = requests.request(
                action,
                url=request_vals['url'],
                headers=request_vals['headers'],
                data=payload,
                files=files,
                timeout=10,
            )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:

            msg = """Erro de conexão/timeout: Não foi possivel se conectar ao PlugNotas.
            O serviço PlugNotas offline ou sofrendo instabilidade em sua conexão.
            Por favor, tente mais tarde."""

            raise UserError(msg) from exc

        res = json.loads(response.text)

        if response.status_code in (200, 201):
            tecnospeed_certificado_id = res['data']['id']

        # 409: conflito de registros
        elif response.status_code == 409:
            tecnospeed_certificado_id = res['error']['data']['current']['id']

        else:
            raise UserError(res['error']['message'])

        if self.tecnospeed_sandbox_active:
            self.tecnospeed_certificado_id_sandbox = tecnospeed_certificado_id
        else:
            self.tecnospeed_certificado_id_producao = tecnospeed_certificado_id

    def action_post_tecnospeed_company(self):
        """Realiza o POST e PATCH para obter/atualizar
        o cadastro da empresa no PlugNotas (tecnospeed). O ambiente
        selecionado depende se o ambiente de 'sandbox' esta ou não ativo.

        Raises:
            UserError: Token de usuario ausento para ambiente de produção/homologação
            UserError: Erro de conexão com o ambiente do PlugNotas
            UserError: Erro na montagem dos parametros da requisição
            UserError: Erro retornado pelo PlugNotas, como ID de certificado inexistente, por exemplo.
        """

        company_vals = self._prepare_company_values()
        # request_vals = self.get_tecnospeed_request_vals(subdomain=f"empresa/{re.sub('[^0-9]', '', self.cnpj_cpf or '')}")
        request_vals = self.get_tecnospeed_request_vals(subdomain="empresa")

        payload = json.dumps(company_vals)

        try:

            response = requests.request(
                'POST',
                url=request_vals['url'],
                headers=request_vals['headers'],
                data=payload,
                timeout=10,
            )

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as exc:

            msg = """Erro de conexão/timeout: Não foi possivel se conectar ao PlugNotas.
            O serviço PlugNotas offline ou sofrendo instabilidade em sua conexão.
            Por favor, tente mais tarde."""

            raise UserError(msg) from exc

        res = json.loads(response.text)

        import ipdb; ipdb.set_trace()  # noqa
        

        if response.status_code == 400:
            raise UserError(f"{res['message']}:{res['error']['data']}")

        elif response.status_code != 200:
            raise UserError(f"{res['error']['message']}:{res['error']['data']}")

    def _prepare_company_values(self):
        """Monta dict com valores para cadastro da empresa no PlugNotas

        Returns:
            dict: dicionario com os campos da empresa
        """
        # A numeracao do tipo fiscal da empresa nao bate com a numeracao
        # usada na tecnospeed. Sendo assim tivemos que realizar o mapeamento abaixo
        if self.fiscal_type in ('1', '2', '4'):
            regime_tributario = self.fiscal_type

        elif self.fiscal_type == '5':
            regime_tributario = '3'

        else:
            regime_tributario = '0'

        certificado = self.tecnospeed_certificado_id_sandbox if self.tecnospeed_sandbox_active else self.tecnospeed_certificado_id_producao

        values = {
            "cpfCnpj": re.sub('[^0-9]', '', self.cnpj_cpf or ''),
            # "inscricaoMunicipal": re.sub('[^0-9]', '', self.inscr_mun or ''),
            # "inscricaoEstadual": re.sub('[^0-9]', '', self.inscr_est or ''),
            "razaoSocial": self.legal_name or '',
            "nomeFantasia": self.name,
            "certificado": certificado,
            "simplesNacional": self.fiscal_type in ('1', '2'),
            "regimeTributario": int(regime_tributario),
            # "incentivoFiscal": self.tecnospeed_incentivo_fiscal,
            # "incentivadorCultural": self.tecnospeed_incentivador_cultural,
            "regimeTributarioEspecial": int(self.tecnospeed_regime_tributacao),
            "endereco": {
                "bairro": self.district,
                "cep": self.zip,
                "codigoCidade": f'{self.state_id.ibge_code}{self.city_id.ibge_code}' or '',
                "estado": self.state_id.code,
                "logradouro": self.street,
                "numero": self.number or '',
                "tipoLogradouro": "Rua",
                # "codigoPais": self.country_id.code,
                "complemento": self.street2 or '',
                # "descricaoCidade": self.city_id.name,
                # "descricaoPais": "Brasil",
                # "tipoBairro": "Bairro"
            },
            # "telefone": {
            #     "numero": self.phone or '',
            # },
            "email": self.email or '',
            "nfse": {
                "ativo": True,
                "tipoContrato": 0,
                "config": {
                    "producao": False if self.tipo_ambiente_nfse == '2' else True,
                    "nfseNacional": False,
                    "email": {
                        "envio": False
                    },
                }
            },
            "nfe": {
                "ativo": False,
                "tipoContrato": 0,
            },
            "nfce": {
                "ativo": False,
                "tipoContrato": 0,
            },
            "mdfe": {
                "ativo": False,
                "tipoContrato": 0,
            }
        }

        return values
