from odoo import api, fields, models
from odoo.addons.br_account_einvoice_tecnospeed.models.const import SANDBOX_TOKEN


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tecnospeed_certificado_id_sandbox = fields.Char(
        string='Tecnospeed Certificado ID (sandbox)',
        default=SANDBOX_TOKEN,
    )

    tecnospeed_certificado_producao = fields.Char(
        string='Tecnospeed Certificado ID (producao)',
    )

    @api.model
    def get_values(self):
        """Retorna e atualiza os campos do res.config.settings a partir
         dos parametros de sistema.

        Returns:
            dict: campos do res.config.settings a serem atualizados
        """
        res = super(AccountConfigSettings, self).get_values()

        get_param = self.env['ir.config_parameter'].sudo().get_param

        tecnospeed_certificado_id_sandbox = get_param(
            'br_account_einvoice.tecnospeed_certificado_id_sandbox',
        )

        tecnospeed_certificado_producao = get_param(
            'br_account_einvoice.tecnospeed_certificado_producao',
        )

        res.update({
            'tecnospeed_certificado_id_sandbox': tecnospeed_certificado_id_sandbox,
            'tecnospeed_certificado_producao': tecnospeed_certificado_producao,
        })

        return res

    @api.multi
    def set_values(self):
        """Grava valores registrados no res.config.settings para os respectivos
        campos dos parâmetros de sistema.
        """
        super(AccountConfigSettings, self).set_values()

        set_param = self.env['ir.config_parameter'].sudo().set_param

        # we store the repr of the values, since the value of the parameter is
        # a required string
        set_param(
            'br_account_einvoice.tecnospeed_certificado_id_sandbox',
            repr(self.tecnospeed_certificado_id_sandbox)
        )

        set_param(
            'br_account_einvoice.tecnospeed_certificado_producao',
            repr(self.tecnospeed_certificado_producao),
        )
