# © 2018 Michell Stuttgart, Multidados
import logging
import re
import requests

import brazilcep

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class BrZipAbstract(models.AbstractModel):
    _name = 'br.zip.abstract'
    _description = 'Abstract class to add zip search'

    search_cep_exception = fields.Char(string='Search CEP message')

    @api.onchange('zip')
    def _onchange_zip(self):
        """Realiza a busca dos dados de endereço de acordo com
        o CEP inserido.
        """
        cep = re.sub('[^0-9]', '', self.zip or '')
        if len(cep) == 8:
            self.zip = f"{cep[0:5]}-{cep[5:8]}"
            self.update(self.get_address())

    @api.multi
    def get_address_from_zip(self, zip_code):
        """Realiza a consulta de CEP de acordo com o ambiente
        escolhido e retorna os dados do endereço relativo ao CEP.

        Arguments:
            zip_code {str} -- Código do CEP para consulta

        Raises:
            UserError -- Quando o CEP não é valido
            UserError -- Quando ocorre erro na conexão com o Webservice

        Returns:
            dict -- Dados dos endereços buscado.
                zip_code {str} -- codigo do cep
                street {str} -- nome do logradouro
                district {str} -- nome do bairro
                city {str} -- nome da cidade
                state_code {str} -- código do estado, i.e, 'MG', 'SP" e etc
                country_code {str} -- código do país, i.e, 'BR'
        """

        values = {
            # 'zip_code': '',
            'street': '',
            'district': '',
            'city': '',
            'state_code': '',
            'country_code': 'BR',
        }

        try:

            # Outras opções são 'WebService.VIACEP' e 'WebService.Correios'
            # Para mais detalhes consultar doc: https://github.com/mstuttgart/brazilcep
            res = brazilcep.get_address_from_cep(zip_code, webservice=brazilcep.WebService.VIACEP)

            values.update({
                'zip_code': res['cep'].replace('-', ''),
                'street': res['street'],
                'district': res['district'],
                'city': res['city'],
                'state_code': res['uf'],
                'country_code': 'BR',
            })

            return values

        except brazilcep.exceptions.InvalidCEP:
            return {
                'street': 'CEP buscado é inválido: %s' % zip_code,
            }
            # raise UserError('CEP buscado é inválido: %s' % zip_code)

        except brazilcep.exceptions.CEPNotFound:
            values.update({
                'street': 'CEP buscado é inválido: %s' % zip_code,
            })
            return values
            # raise UserError('CEP %s não encontrado' % zip_code)

        # except requests.exceptions.ConnectionError as errc:
        #     raise UserError('Erro de conexão com o servidor de CEPs. Por favor, tente mais tarde. %s' % errc)

        # except requests.exceptions.Timeout as errt:
        #     raise UserError('Tempo de consulta expirado: %s. Contate o administrado do sistema' % errt)

        # except requests.exceptions.HTTPError as errh:
        #     raise UserError('Erro na requisição HTTP: %s. Contate o administrado do sistema' % errh)

        # except Exception as exc:
        #     raise UserError('Ocorreu um erro desconhecido. Contate o administrado do sistema. Erro: %s' % exc) # noqa

    @api.multi
    def create_br_zip_from_address(self, zip_code, street, district, city, state_code, country_code):  # noqa
        """Cria um objeto br.zip a partir dos parametros fornecidos.

        Arguments:
            zip_code {str} -- Codigo de CEP
            street {str} -- Nome do logradouro
            district {str} -- Nome do bairro
            city {str} -- Nome da cidade
            state_code {str} -- Codigo do estado
            country_code {str} -- Codigo do país

        Returns:
            BrZip -- Nova instancia de br.zip
        """

        values = {
            'zip': zip_code,
            'street': street,
            'district': district,
            'state_code': state_code,
        }

        # Search Brazil id
        country_ids = self.env['res.country'].search(
            [('code', '=', country_code)])

        # Search state with state_code and country id
        state_ids = self.env['res.country.state'].search([
            ('code', '=', state_code),
            ('country_id', 'in', country_ids.ids)])

        # search city with name and state
        city_ids = self.env['res.state.city'].search([
            ('name', '=', city),
            ('state_id', 'in', state_ids.ids)])

        if city_ids:
            values.update({
                'country_id': city_ids[0].state_id.country_id.id,
                'state_id': city_ids[0].state_id.id,
                'city_id': city_ids[0].id,
                'ibge_code': city_ids[0].ibge_code,
                'country_code': city_ids[0].state_id.country_id.code,
            })
        else:
            _logger.error(
                'Cidade retornada pela consulta de CEP não existe no sistema',
                exc_info=True)

        return self.env['br.zip'].create(values)

    @api.multi
    def get_address(self):
        """Realiza a consulta de CEP, cria uma nova entrada
        da model br.zip e retorna uma ditc contendo os valores do endereço
        recem consultado.

        Returns:
            dict -- Campos de endereço inicializados com valores do CEP.
        """
        return self._get_address(self.zip)

    @api.multi
    def _get_address(self, zipcode):
        """Realiza a consulta de CEP, cria uma nova entrada
        da model br.zip e retorna uma ditc contendo os valores do endereço
        recem consultado.

        Returns:
            dict -- Campos de endereço inicializados com valores do CEP.
        """
        res = {}

        # Remove pontuacao do CEP
        zip_code = re.sub('[^0-9]', '', zipcode or '')

        # Realizamos a busca pelo cep na tabela do br.zip
        br_zip = self.env['br.zip'].search([('zip', '=', zip_code)], limit=1)

        if not br_zip:
            # Realiza a consulta de CEP
            address = self.get_address_from_zip(zip_code=zip_code)

            if 'zip_code' not in address:
                values = {
                    'street': '',
                    'district':  '',
                    'city_id': False,
                    'state_id': False,
                    'search_cep_exception': address['search_cep_exception']
                    # 'country_id': self.country_id and self.country_id.id or '',
                }

                return values

            # Cria um objeto br.zip
            br_zip = self.create_br_zip_from_address(**address)

            # Converte os campo do br.zip em dicionario
            res = br_zip.convert_address_fields_to_dict()
        else:
            res = br_zip.convert_address_fields_to_dict()

        return res
