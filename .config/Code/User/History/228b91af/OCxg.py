import base64
import json
import urllib

import requests

from odoo import fields, models
from odoo.addons.br_nfse_tecnospeed.models.const import SANDBOX_TOKEN, TRIBUTACAO, URL_PRODUCAO, URL_SANDBOX
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    webservice_nfse = fields.Selection(selection_add=[
        ('nfse_tecnospeed', 'Nota Fiscal Serviço (Tecnospeed)'),
    ])

    nfse_tecnospeed_regime_tributacao = fields.Selection(
        selection=TRIBUTACAO,
        default='1',
        string='Regime de Tributação (Tecnospeed)',
        help='Código de identificação do regime especial de tributação',
    )

    nfse_tecnospeed_incentivador_cultural = fields.Boolean(
        string='Incentivador Cultural (Tecnospeed)',
    )

    nfse_tecnospeed_incentivo_fiscal = fields.Boolean(
        string='Incentivo Fiscal (Tecnospeed)',
    )

    tecnospeed_sandbox_active = fields.Boolean(
        string='Sandbox active (developer)',
        help="""Ativa modo sandbox para desenvolvimento. Com esse modo ativado,
        as resposta do webservice sao padronizadas pela Tecnospeed"""
    )

    tecnospeed_certificado_sandbox = fields.Char(
        string='Certificado ID (sandbox)',
    )

    tecnospeed_certificado_producao = fields.Char(
        string='Certificado ID (producao)',
    )

    tecnospeed_token_sandbox = fields.Char(
        string='Token (sandbox)',
        default=SANDBOX_TOKEN,
    )

    tecnospeed_token_producao = fields.Char(
        string='Token (producao)',
    )

    def get_tecnospeed_request_vals(self, subdomain):

        if self.tecnospeed_sandbox_active:
            url = f'{URL_SANDBOX}'
            token = self.tecnospeed_token_sandbox

        else:
            url = f'{URL_PRODUCAO}'
            token = self.tecnospeed_token_producao

        headers = {
            # 'Content-Type': 'application/json',
            'x-api-key': token,
        }

        return {
            'url': urllib.parse.urljoin(url, subdomain),
            'headers': headers,
        }

    def action_get_tecnospeed_certificado(self):

        # ambiente de desenvolvimento sandbox
        if self.tecnospeed_sandbox_active:

            # atualiza ID certificado
            if self.tecnospeed_certificado_sandbox:
                action = 'PUT'
                request_vals = self.get_tecnospeed_request_vals(subdomain=f'certificado/{self.tecnospeed_certificado_sandbox}')  # noqa

            # cadastra certificado e obtem seu ID
            else:
                action = 'POST'
                request_vals = self.get_tecnospeed_request_vals(subdomain='certificado')

        else:

            if not self.tecnospeed_token_producao:
                raise UserError('TOKEN de usuário Tecnospeed ausente')

            # atualiza ID certificado
            if self.tecnospeed_certificado_producao:
                action = 'PUT'
                request_vals = self.get_tecnospeed_request_vals(subdomain=f'certificado/{self.tecnospeed_certificado_producao}')  # noqa

            # cadastra certificado e obtem seu ID
            else:
                action = 'POST'
                request_vals = self.get_tecnospeed_request_vals(subdomain='certificado')


        # Salvamos o certificado em disco porque a tecnospeed aceita
        # apenas o path do certificado
        with open('/tmp/cert.pfx', 'wb+') as fp:
            fp.write(base64.b64decode(self.nfe_a1_file))

        files = [
            ('arquivo', ('cert.pfx', open('/tmp/cert.pfx', 'rb'), 'application/octet-stream'))
        ]

        payload = {
            'senha': self.nfe_a1_password,
            'arquivo': 'cert.pfx',
        }

        # request_vals['headers']['Content-Type'] = ''

        response = requests.request(
            action,
            url=request_vals['url'],
            headers=request_vals['headers'],
            data=payload,
            files=files,
            timeout=1,
        )

        res = json.loads(response.text)

        if not response.ok:
            raise UserError(f'Ocorreu um erro: {response.text}')

        if response.status_code not in (200, 201):
            raise UserError(res['error']['message'])

        if self.tecnospeed_sandbox_active:
            self.tecnospeed_certificado_sandbox = res['data']['id']
        else:
            self.tecnospeed_certificado_producao =  res['data']['id']






