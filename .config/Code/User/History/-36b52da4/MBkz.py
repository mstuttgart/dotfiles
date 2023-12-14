

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
        res = super(AccountConfigSettings, self).get_values()

        get_param = self.env['ir.config_parameter'].sudo().get_param

        tecnospeed_certificado_sandbox = get_param('br_account_einvoice.tecnospeed_certificado_sandbox', default='False')
        tecnospeed_certificado_producao = get_param('br_account_einvoice.tecnospeed_certificado_producao', default='False')

        # the value of the parameter is a nonempty string
        budget_templ_id = literal_eval(
            get_param('br_account_budget_template.budget_template_id',
                      default='False'))
        if (budget_templ_id and
                not self.env['crossovered.budget.template'].sudo().browse(
                    budget_templ_id).exists()):
            budget_templ_id = False

        res.update(
            budget_templ_id=budget_templ_id,
        )
        
        return res

    @api.multi
    def set_values(self):
        super(AccountConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        # we store the repr of the values, since the value of the parameter is
        # a required string
        set_param('br_account_budget_template.budget_template_id',
                  repr(self.budget_templ_id.id))
