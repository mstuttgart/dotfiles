from odoo import api, models
from odoo.exceptions import UserError


class InvoiceElectronic(models.Model):
    _inherit = 'invoice.electronic'

    @api.multi
    def get_mail_template_items(self):
        """Retorna os templates relacionado a cada doc. eletronico
        de acordo com o status do mesmo.

        Raises:
            UserError -- Se um dos templates de confirmação não existir.
            UserError -- Se um dos templates de cancelamento não existir.

        Returns:
            dict -- Dict contendo o ID do doc. eletronico e seu respectivo template.
        """
        res = super(InvoiceElectronic, self).get_mail_template_items()

        # Filtramos os doc. eletronicos que foram confirmados
        # e são NFSe
        nfse_done = self.filtered(
            lambda r: r.state == 'done' and r.model == '001')

        # Percorremos a nfse que foram confirmadas
        for nfse in nfse_done:

            mail_template = nfse.company_id.nfse_email_template_id

            if mail_template:

                # Guardamos o template reference ao doc. eletronico
                res[nfse.id] = {
                    'mail_template': mail_template,
                    'report_template': nfse.company_id.report_nfse_id,
                    'attachment_ids': [],
                }

            elif self.nfe_engine != 'tecnospeed':
                raise UserError('Modelo de email para NFSe da empresa %s não configurado!' % )

        # Filtramos os doc. eletronicos que foram cancelados
        # e são NFSe
        nfse_cancel = self.filtered(
            lambda r: r.state == 'cancel' and r.model == '001')

        # Percorremos a nfse que foram canceladas
        for nfse in nfse_cancel:

            mail_template = nfse.company_id.nfse_cancel_email_template_id

            if mail_template:

                # Guardamos o template reference ao doc. eletronico
                res[nfse.id] = res[nfse.id] = {
                    'mail_template': mail_template,
                    'report_template': nfse.company_id.report_nfse_id,
                    'attachment_ids': [],
                }

            elif self.nfe_engine != 'tecnospeed':
                raise UserError('Modelo de email de cancelamento para NFSe da empresa %s não configurado!' % nfse.company_id.name)

        return res
