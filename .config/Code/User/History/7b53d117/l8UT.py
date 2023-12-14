from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    ticket_id = fields.Many2one(
        'helpdesk.support',
        string='Helpdesk Ticket',
        readonly=True,
        ondelete='restrict',
        index=True,
        copy=True
    )

    ticket_product_id = fields.Many2one(
        related='ticket_id.product_id',
    )

    @api.onchange('stage_id')
    def onchange_stage_id(self):
        """Método onchange que fecha o ticket relacionado
        caso o novo estágio esteja com a flag
        close_ticket_and_notify_customer.
        """
        task_id = (hasattr(self, '_origin') and self._origin) or self

        if not self.stage_id.close_ticket_and_notify_customer:
            return

        if not task_id.ticket_id:
            return

        emails = self.get_email_participants()

        # Flag para indicar que o fechamento do ticket partiu
        # de uma tarefa
        ctx = {
            'close_ticket_from_task_id': task_id.id,
        }

        task_id.ticket_id.sudo().with_context(**ctx).set_to_close(send_email=False)
        task_id.ticket_id.sudo().send_email_closed_ticket(
            emails, self.stage_id.customer_warning_message)

    def get_email_participants(self):
        """Método que retorna a uma string separada por
        virgula com a lista de emails dos seguidores da
        tarefa e do parceiro.

        Returns:
            string: retorna a lista de emails separados por
            vírgula.
        """
        partners = self.message_follower_ids.mapped('partner_id')
        emails = partners.mapped('email')
        emails.append(self.partner_id.email)
        emails = list(filter(None, emails))

        return ','.join(emails)

    def _compute_attached_docs_count(self):
        """ Counts the number of attached documents and
            assigns in doc_count field.
        """
        attachment_obj = self.env['ir.attachment']
        for task in self:
            task.doc_count = attachment_obj.search_count([
                '|',
                '&', ('res_model', '=', 'project.task'), ('res_id', 'in', task.ids),
                '&', ('res_model', '=', 'helpdesk.support'), ('res_id', '=', task.ticket_id.id)])

    @api.multi
    def attached_docs_view_action(self):
        """ Método que retorna a action que leva para a view dos anexos da tarefa e
        do ticket relacionado. Altera o domain da função original.
        Returns:
            dict: valores para a 'ir.actions.act_window' que abre a view dos anexos.
        """
        res = super(ProjectTask, self).attached_docs_view_action()
        if self.ticket_id:
            domain = ['|',
                      '&', ('res_model', '=',
                            'project.task'), ('res_id', 'in', self.ids),
                      '&', ('res_model', '=', 'helpdesk.support'), ('res_id', '=', self.ticket_id.id)]

            res['domain'] = domain
        return res

    def _create_support_line(self, material):
        """ Método para criar uma linha de fatura para um material
        planejado ou consumido pela tarefa que está sendo Concluída.

        Args:
            material ('consumed.material') ou ('material.plan'): material
                que está sendo transformado em linha de fatura de ticket

        Raises:
            ValueError: Se a model do parâmetro 'material' não estiver no
                conjunto {'consumed.material', 'material.plan'}

        Returns:
            'support.invoice.line': Linha de fatura do ticket criada.
        """
        if material._name == 'material.plan':
            vals = {
                'is_material_plan': True,
                'material_plan_id': material.id,
            }
        elif material._name == 'consumed.material':
            vals = {
                'is_material_consumed': True,
                'material_consumed_id': material.id,
            }
        else:
            raise ValueError(
                "'material' argument must be in ('material.plan', 'consumed.material')")

        vals.update({
            'ticket_task_id': self.id,
            'support_id': self.ticket_id.id,
            'product_id': material.product_id.id,
            'name': material.description,
            'quantity': float(material.product_uom_qty),
            'product_uom_qty': material.product_uom_qty,
            'product_uom': material.product_uom_id.id,
            'price_unit': material.product_id.lst_price,
        })
        return self.env['support.invoice.line'].create(vals)

    def _prepare_support_lines(self, materials):
        """ Método que sincroniza linhas de fatura de produtos com linhas
        de materiais das tarefas.

        Args:
            materials (material.plan) ou (consumed.material): recordset dos materiais consumidos ou planejados da tarefa
            creating (bool, optional): Valor para saber se o record está sendo criado ou editado. Defaults to False.

        Raises:
            ValueError: Se a classe do materials for diferente de (material.plan) ou (consumed.material)
        """
        if materials:
            # Procura pelas linhas de fatura de suporte existentes que já possuem
            # um orçamento criado que possa adicionar a nova linha
            domain = [
                ('support_id', '=', self.ticket_id.id),
                ('ticket_task_id', '=', self.id),
                ('sale_order_id.state', 'in', ('draft', 'sent')),
            ]
            support_line_id = self.env['support.invoice.line'].search(
                domain, limit=1)

            # Obtendo uma Sale Order que está no estágio de Cotação para criar
            # uma nova order_line da nova linha que está sendo adicionada
            sale_order = support_line_id.sale_order_id

            # Criando linhas de fatura do ticket
            for line in materials:
                self._create_support_line(line)

            # Criando 'sale.order.line' dos novos materiais adicionados
            if sale_order:
                self.ticket_id._prepare_sale_order_line(sale_order)

    @api.multi
    def write(self, vals):
        """ Altera o método write para atualizar as linhas de produto do ticket
        ao alterar as linhas de produtos consumidos e planejados das tarefas.

        Args:
            vals (dict): Valores que foram alterados no registro

        Returns:
            project.task : Tarefa alterada
        """
        res = super(ProjectTask, self).write(vals)
        for rec in self:
            if rec.ticket_id:
                if 'stage_id' in vals:
                    if rec.stage_state == 'done':
                        # Atualiza linhas de fatura com materiais da tarefa
                        rec._prepare_support_lines(rec.material_plan_ids.filtered(lambda m: not m.invoiced)) # noqa
                        rec._prepare_support_lines(rec.consumed_material_ids.filtered(lambda m: not m.invoiced)) # noqa

                if 'timesheet_ids' in vals.keys():
                    # Relaciona planilha de hora ao ticket
                    for line in rec.timesheet_ids:
                        line.support_request_id = rec.ticket_id
        return res

    @api.model
    def create(self, vals):
        """ Altera o método create para criar as linhas de produto do ticket
        com base nas linhas de produtos consumidos e planejados das tarefas.

        Args:
            vals (dict): Valores de criação do registro

        Returns:
            project.task : Tarefa criada
        """
        res = super(ProjectTask, self).create(vals)
        if res.ticket_id:
            if res.stage_state == 'done':
                res._prepare_support_lines(
                    res.material_plan_ids.filtered(lambda m: not m.invoiced))
                res._prepare_support_lines(
                    res.consumed_material_ids.filtered(lambda m: not m.invoiced))

            if 'timesheet_ids' in vals.keys():
                # Relaciona planilha de hora ao ticket
                for line in res.timesheet_ids:
                    line.support_request_id = res.ticket_id
        return res

    def get_company_address_report(self):
        """ Método para obter as linhas utilizadas no relatório de OS da tarefa
        na área das informações da empresa. É retornado uma tupla, em que cada
        posição é uma linha no relatório.

        Returns:
            tuple: [0] - string com endereço da empresa
                   [1] - string com dados da empresa
        """
        company = self.company_id

        # linha de endereço
        line1 = f"{company.street}, {company.number} - {company.street2} - {company.district}" \
                f" - {company.city_id.name}/{company.state_id.code}"

        # linha de informações
        line2 = f"{company.phone} - CNPJ: {company.cnpj_cpf} - IE: {company.inscr_est}"

        return line1, line2

    def report_description(self):
        """ Método para obter a descrição sem a quebra de linha padrão.

        Returns:
            string: descrição da tarefa no formato html, mas sem a primeira quebra de linha.
        """
        if self.description:
            return self.description.replace('<br>', '', 1)
        return ''
