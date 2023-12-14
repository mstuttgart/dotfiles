from odoo import fields, models
from odoo.addons.br_nfse_goiania.models.const import INC_CULTURAL


class ResCompany(models.Model):
    _inherit = 'res.company'

    webservice_nfse = fields.Selection(selection_add=[
        ('nfse_goiania', 'Nota Fiscal Serviço (goiania)'),
    ])

    nfse_goiania_incentivador_cultural = fields.Selection(
        selection=INC_CULTURAL,
        default='2',
        string='Incentivador Cultural (goiania)',
    )
