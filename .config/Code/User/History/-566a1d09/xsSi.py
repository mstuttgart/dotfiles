# © 2012  Renato Lima - Akretion
# © 2016 Danimar Ribeiro, Trustcode
# © 2018 Michell Stuttgart, Multidados
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BrZip(models.Model):
    _name = 'br.zip'
    _rec_name = 'zip'
    _description = """Este objeto persiste todos os códigos postais que
    podem ser utilizados para pesquisar e auxiliar o preenchimento dos
    endereços."""

    zip = fields.Char(string='CEP', size=8, required=True, index=True)
    street = fields.Char(string='Logradouro', size=72)
    district = fields.Char(string='Bairro', size=72)
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state',
                               string='Estado',
                               domain="[('country_id','=',country_id)]")
    city_id = fields.Many2one('res.state.city',
                              string='Cidade',
                              required=False,
                              domain="[('state_id','=',state_id)]")
    state_code = fields.Char(string='Código Estado', size=2)
    ibge_code = fields.Char(string='Código IBGE', size=7, index=True)
    country_code = fields.Char(string='Código Pais', size=2, default='BR')

    @api.multi
    def convert_address_fields_to_dict(self):
        """Cria um dict com os valores dos campos da model.
        Este metodo facilita a conversao dos campos de br.zip para
        formato facil de manipular de modo a utiliza-los para
        atualizar os campos de endereço de outros models.

        Returns:
            dict -- contem os valores dos campos da model.
        """
        self.ensure_one()

        zip_code = f'{self.zip[0:5]}-{self.zip[5:8]}' if self.zip else ''

        values = {
            'zip': zip_code,
            'street': self.street or '',
            'district': self.district or '',
            'city_id': self.city_id and self.city_id.id or '',
            'state_id': self.state_id and self.state_id.id or '',
            'country_id': self.country_id and self.country_id.id or '',
        }

        return values
