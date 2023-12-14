

from odoo import api, fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tecnospeed_certificado_sandbox = fields.Char(
        string='Tecnospeed Certificado ID (sandbox)',
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

        tecnospeed_certificado_sandbox = get_param(
            'br_account_einvoice.tecnospeed_certificado_sandbox',
            default='False'
        )

        tecnospeed_certificado_producao = get_param(
            'br_account_einvoice.tecnospeed_certificado_producao',
            default='False',
        )

        res.update({
            'tecnospeed_certificado_sandbox': tecnospeed_certificado_sandbox,
            'tecnospeed_certificado_producao': tecnospeed_certificado_producao,
        })

        return res

    @api.multi
    def set_values(self):
        """_summary_
        """
        super(AccountConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        # we store the repr of the values, since the value of the parameter is
        # a required string
        set_param('br_account_budget_template.budget_template_id',
                  repr(self.budget_templ_id.id))
