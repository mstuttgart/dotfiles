from odoo import models

class ThemeJtCorporate2201(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_bootswatch_post_copy(self, mod):
        self.disable_view('website_theme_install.customize_modal')
