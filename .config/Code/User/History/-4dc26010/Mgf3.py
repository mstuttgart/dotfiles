from unittest import mock

import brazilcep
import requests

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestBrZipAbstract(TransactionCase):

    def setUp(self):
        super(TestBrZipAbstract, self).setUp()

    @mock.patch('odoo.addons.br_zip.models.br_zip_abstract.brazilcep.get_address_from_cep')
    def test_get_address_from_zip_success(self, mk):

        mk.return_value = {
            'cep': '37503130',
            'street': 'Rua Geraldino Campista',
            'district': 'Santo Antônio',
            'city': 'Itajubá',
            'uf': 'MG',
        }

        res = self.env['br.zip.abstract'].get_address_from_zip('37503130')

        self.assertEqual(res['zip_code'], '37503130')
        self.assertEqual(res['street'], 'Rua Geraldino Campista')
        self.assertEqual(res['district'], 'Santo Antônio')
        self.assertEqual(res['city'], 'Itajubá')
        self.assertEqual(res['state_code'], 'MG')
        self.assertEqual(res['country_code'], 'BR')

    @mock.patch('odoo.addons.br_zip.models.br_zip_abstract.brazilcep.get_address_from_cep')
    def test_get_address_from_zip_excecao_pycepcorreios(self, mk):

        mk.side_effect = brazilcep.exceptions.InvalidCEP()

        address = self.env['br.zip.abstract'].get_address_from_zip('37503130')

        self.assertEqual(address['search_cep_exception'], 'CEP buscado é inválido: 37503130')

        # ------------------------------------

        mk.side_effect = brazilcep.exceptions.CEPNotFound()

        address = self.env['br.zip.abstract'].get_address_from_zip('37503130')

        self.assertEqual(address['search_cep_exception'], 'CEP 37503130 não encontrado')

        # ------------------------------------

        mk.side_effect = requests.exceptions.ConnectionError()

        address = self.env['br.zip.abstract'].get_address_from_zip('37503130')

        self.assertEqual(address['search_cep_exception'], 'Erro de conexão com o servidor de CEPs. Por favor, tente mais tarde. ')

        # ------------------------------------


        # with self.assertRaises(UserError):
        #     self.env['br.zip.abstract'].get_address_from_zip('37503130')

        # mk.side_effect = requests.exceptions.Timeout()

        # with self.assertRaises(UserError):
        #     self.env['br.zip.abstract'].get_address_from_zip('37503130')

        # mk.side_effect = requests.exceptions.HTTPError()

        # with self.assertRaises(UserError):
        #     self.env['br.zip.abstract'].get_address_from_zip('37503130')

        # mk.side_effect = brazilcep.exceptions.BrazilCEPException()

        # with self.assertRaises(UserError):
        #     self.env['br.zip.abstract'].get_address_from_zip('37503130')

        # mk.side_effect = Exception()

        # with self.assertRaises(UserError):
        #     self.env['br.zip.abstract'].get_address_from_zip('37503130')

    def test_create_br_zip_from_address(self):

        values = {
            'zip_code': '37503130',
            'street': 'Rua Geraldino Campista',
            'district': 'Santo Antônio',
            'city': 'Itajubá',
            'state_code': 'MG',
            'country_code': 'BR',
        }

        br_zip = self.env['br.zip.abstract'].create_br_zip_from_address(
            **values)

        self.assertEqual(br_zip._name, 'br.zip')

        self.assertEqual(br_zip.zip, '37503130')
        self.assertEqual(br_zip.street, 'Rua Geraldino Campista')
        self.assertEqual(br_zip.district, 'Santo Antônio')
        self.assertEqual(br_zip.city_id.name, 'Itajubá')
        self.assertEqual(br_zip.state_id.code, 'MG')
        self.assertEqual(br_zip.country_id.code, 'BR')
