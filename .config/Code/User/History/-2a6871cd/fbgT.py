from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_mode_id = fields.Many2one(
        string="Modo de pagamento",
        track_visibility='onchange',
        comodel_name='payment.mode'
    )

    fiscal_position_id = fields.Many2one(
        'account.fiscal.position',
        related='invoice_id.fiscal_position_id',
        ondelete='restrict',
        store=True,
        index=True
    )

    followup_line_id = fields.Many2one(
        'account_followup.followup.line',
        'Follow-up Level',
        ondelete='restrict',
        index=True
    )

    followup_date = fields.Date(
        'Latest Follow-up',
        index=True
    )

    partner_cpf_cnpj = fields.Char(
        string='Partner CNPJ/CPF',
        related='partner_id.cnpj_cpf'
    )

    partner_legal_name = fields.Char(
        string='Partner Legal Name',
        related='partner_id.legal_name'
    )

    document_image = fields.Binary(
        string='Image Document',
        help='Financial Document Image'
    )

    note = fields.Text(
        string='Note',
        readonly=True
    )

    writedown_date = fields.Date(
        string='Retirement Date',
        readonly=True
    )

    payment_user_id = fields.Many2one(
        string='Payment made by',
        comodel_name='res.users',
        readonly=True,
        help='Indicates the user who made the payment.'
    )

    discharged_move_ids = fields.One2many(
        string='Linked Movements',
        comodel_name='account.move',
        inverse_name='ref_move_id'
    )

    payment_ids = fields.One2many(
        string='Payments',
        comodel_name='account.payment',
        inverse_name='move_id'
    )

    payment_datetime = fields.Datetime(
        string='Paid in',
        index=True,
    )

    reconcile_user_id = fields.Many2one(
        string='Conciliation performed by',
        comodel_name='res.users',
        readonly=True,
        help='Indicates the user who carried out the journal line reconciliation.'
    )

    reconcile_datetime = fields.Datetime(
        string='reconciled in',
        readonly=True
    )

    amount_payment_value = fields.Monetary(
        string='Amount Payment'
    )

    title_status = fields.Selection(
        string="Status do Título",
        compute='_compute_title_status',
        track_visibility='onchange',
        search='_search_late',
        selection=[
            ('expiring', 'Expiring'),
            ('expire_today', 'Expire Today'),
            ('expired', 'Expired'),
            ('anticipated', 'Anticipated'),
            ('paid_day', 'Paid on the day'),
            ('late', 'Late'),
            ('cancelled', 'Cancelled'),
            ('payment_lost', 'Payment Lost'),
            ('renegotiated', 'Renegotiated'),
            ('discounted_title', 'Discounted Title'),
            ('unknown', 'Unknown'),
        ]
    )

    invoice_number = fields.Integer(
        string='Invoice Number',
        related='invoice_id.internal_number',
        store=True
    )

    def _get_default_stage_id(self):
        """ Gives minimum sequence stage
        Returns:
            Int -> retorna o menor ID possível para o estagio.
        """
        stages = self.env['account.move.stage'].search([], order="sequence, id desc", limit=1).id # noqa
        return stages

    custom_stage_id = fields.Many2one(
        'account.move.stage',
        string="Stage",
        ondelete='restrict',
        track_visibility='onchange',
        index=True,
        default=_get_default_stage_id,
        copy=False
    )

    custom_stage_color = fields.Many2many(
        'account.move.stage',
        compute='_compute_stage_color',
        readonly=True
    )

    receiving_commission = fields.Char(
        string='Receiving Commission'
    )

    commission_move_id = fields.Many2one(
        comodel_name='account.move'
    )

    # Utilizado para Faturamento do C/C
    reference_invoice_id = fields.Many2one(
        string='Account Invoice',
        comodel_name='account.invoice'
    )

    # Utilizado para Pagamento do C/C
    payment_invoice_id = fields.Many2one(
        string='Payment Invoice',
        comodel_name='account.invoice'
    )

    res_partner_bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Partner Account Bank'
    )

    receive_status = fields.Selection(
        string='Receive Status',
        selection=[
            ('1', 'To Receive'),
            ('2', 'Receive'),
            ('3', 'In Analise'),
        ],
        default='1'
    )

    entry_source = fields.Selection(
        string='Entry Source',
        selection=[
            ('manual', 'Manual'),
            ('integration', 'Integration'),
        ],
        default='manual',
        help="""Store source entry, manual or integration if entry was manually created"""
    )

    @api.multi
    @api.depends('custom_stage_id')
    def _compute_stage_color(self):
        """Método compute para popular o campo many2many
        custom_stage_color, nesse campo, que estárá como tag,
        o usuário poderá escolher a cor que deseja para o
        marcador.
        """
        for rec in self:
            if rec.custom_stage_id:
                rec.custom_stage_color = rec.custom_stage_id.stage_color_ids

    @api.multi
    def action_register_payment(self):
        self.ensure_one()

        view_id = self.env.ref('br_account_payment.view_br_account_payment_form').id # noqa
        receivable = (self.account_type == 'receivable')

        ctx = {
            'default_amount': self.amount - self.amount_payment_value,
            'default_partner_type': 'customer' if receivable else 'supplier',
            'default_partner_id': self.partner_id.id,
            'default_communication': f'{self.name} - {str(self.parcel_id.name)}',
            'default_payment_type': 'inbound' if receivable else 'outbound',
            'default_move_id': self.id,
            'default_launch_journal_id': self.journal_id.id,
            'default_financial_identifier': self.financial_identifier,
            'default_account_group_id': self.account_group_id.id if self.account_group_id else False,
        }

        if self.invoice_id:
            ctx['default_invoice_ids'] = [(4, self.invoice_id.id)]  # noqa

        # move_reference passado por contexto para uso futuro em
        # metodo 'create' de 'account_move' para referenciamento
        ctx['move_reference'] = self.id

        # journal_type passado por contexto para uso futuro em
        # metodo 'create' de 'account_move' para categorizaçao
        ctx['journal_type'] = 'discharge'

        if ctx['default_partner_type'] == 'customer':
            register_name = _('Register Receive')
        else:
            register_name = _('Register Payment')

        return {
            'name': register_name,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'account.payment',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': ctx
        }

    @api.multi
    def action_alter_date_maturity(self):
        ctx = {
            'default_old_date_maturity': self.date_maturity_current,
            'default_new_date_maturity': self.date_maturity_current,
        }

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.alter.date',
            'view_type': 'form',
            'view_mode': 'form',
            'context': ctx,
            'views': [(False, "form")],
            'target': 'new',
        }

    @api.multi
    def action_alter_operation(self):
        ctx = {
            'default_old_payment_mode': self.payment_mode_id.id,
            'default_new_payment_mode': self.payment_mode_id.id,
            'default_old_title_type': self.title_type_id.id,
            'default_new_title_type': self.title_type_id.id,
            'default_old_financial_operation': self.financial_operation_id.id,
            'default_new_financial_operation': self.financial_operation_id.id,
        }

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.alter.operation',
            'view_type': 'form',
            'view_mode': 'form',
            'context': ctx,
            'views': [(False, "form")],
            'target': 'new',
        }

    @api.multi
    @api.depends('account_type', 'date_maturity_current', 'paid_status', 'payment_datetime') # noqa
    def _compute_title_status(self):
        """ This function will set 'title_status' field according to
            informations from title, value can be 'received', 'payed',
            'expire_today', 'expired', 'cancelled', 'late' and 'unknown'
        """
        for am in self:
            dt_now = fields.date.today()

            if am.payment_ids:
                lines_dates = [line.payment_date for line in am.payment_ids.filtered(lambda r: r.state != 'cancelled')] # noqa
                if lines_dates:
                    date_due = max(lines_dates)
                else:
                    am.paid_status = 'open'
                    date_due = fields.Date.from_string('0001-01-01')
            else:
                date_due = fields.Date.from_string('0001-01-01')

            if am.account_type not in am._account_user_type_hook():
                am.title_status = 'unknown'
            elif (am.paid_status == 'paid' and am.payment_datetime and date_due < (am.date_maturity_current or am.date)):
                am.title_status = 'anticipated'
            elif (am.paid_status == 'paid' and am.payment_datetime and date_due == (am.date_maturity_current or am.date)):
                am.title_status = 'paid_day'
            elif (am.paid_status == 'paid' and am.payment_datetime and date_due > (am.date_maturity_current or am.date)):
                am.title_status = 'late'
            elif (am.paid_status in ('open', 'in_negociation', 'partial') and am.date_maturity_current and am.date_maturity_current < dt_now):
                am.title_status = 'expired'
            elif (am.paid_status in ('open', 'in_negociation', 'partial') and am.date_maturity_current and am.date_maturity_current == dt_now):
                am.title_status = 'expire_today'
            elif (am.paid_status in ('open', 'in_negociation', 'partial') and am.date_maturity_current and am.date_maturity_current > dt_now):
                am.title_status = 'expiring'
            elif am.paid_status == 'cancelled':
                am.title_status = 'cancelled'
            elif am.paid_status == 'paid_lost':
                am.title_status = 'payment_lost'
            elif am.paid_status == 'paid_negotiation':
                am.title_status = 'renegotiated'
            elif am.paid_status == 'discounted_title':
                am.title_status = 'discounted_title'
            else:
                am.title_status = 'unknown'

    def _search_late(self, operator, value):
        """ Modulo funciona como domain para filtro na tela.

        Arguments:
            operator {str} -- Operador a ser utilizado no filtro
            value {str} -- Valor do campo utilizado no filtro.

        Returns:
            list -- Condição do filtro(notação polonesa) que corresponda ao
            valor do campo 'title_status'.
        """
        dt_now = fields.date.today()
        recs = []
        domain = []
        domain_operator = False

        if operator == '=':
            if value in ('anticipated', 'paid_day', 'late'):
                domain = [
                    ('paid_status', '=', 'paid'),
                    ('payment_datetime', '!=', False),
                ]

                recs = self.env['account.move'].search(domain)

                if value == 'anticipated':
                    recs = recs.filtered(lambda l: l.payment_datetime.date() < (l.date_maturity_current or l.date)).mapped('id') # noqa
                elif value == 'paid_day':
                    recs = recs.filtered(lambda l: l.payment_datetime.date() == (l.date_maturity_current or l.date)).mapped('id') # noqa
                elif value == 'late':
                    recs = recs.filtered(lambda l: l.payment_datetime.date() > (l.date_maturity_current or l.date)).mapped('id') # noqa
            else:
                if value == 'expired':
                    domain_operator = '<'
                elif value == 'expiring':
                    domain_operator = '>'

                if domain_operator:
                    domain = [
                        ('date_maturity_current', domain_operator, dt_now),
                        ('paid_status', 'in', ('open', 'partial', 'in_negociation')),
                    ]
                    recs = self.env['account.move'].search(domain).mapped('id')

        return [('id', 'in', recs)]

    @api.multi
    def action_negotiation(self):
        """ This function calls action from negotiation wizard, which will
            alter value from current title

        Returns:
            dict -- Action to call 'account.negotiation' wizard
        """
        self.ensure_one()

        res = self.env['ir.actions.act_window'].for_xml_id(
            'br_account_payment', 'action_account_negotiation')

        res['context'] = {'default_negotiated_value': self.amount}

        return res

    def _amount_compute(self):
        super(AccountMove, self)._amount_compute()

        # After negotiation operations, some lines are created to bring balance
        # in move record, only one line represents amount value from move, and
        # this same line generally has the same account in move record.
        for record in self:
            for line in record.line_ids:
                if record.account_id.id == line.account_id.id:
                    record.amount = line.debit or line.credit

    @api.multi
    def open_reconcile_full_view(self):
        """ Esta função chama a ação que abre formulario de conciliamento

        Raises:
            UserError -- Apenas títulos com contas conciliaveis podem ser
            conciliados

        Returns:
            dict -- Ação que chama formulário de 'account.negotiation'
        """
        self.ensure_one()

        # Capturamos a linhas relacionadas ao pagamento da move line
        # selecionada
        if self.account_id.reconcile:
            res = self.env['ir.actions.act_window'].for_xml_id('br_account_payment', 'action_account_negotiation_reconcile') # noqa

            res['context'] = {
                'default_renegotiated_value': self.amount_payment_value,
                'default_negotiated_value': self.amount,
                'paid_status': 'paid_lost',
            }

            return res
        else:
            raise UserError('Apenas títulos pagos podem ser conciliadas!')

    @api.multi
    def action_reverse_payment(self):
        """ Método para estornar uma account.move que foi baixada por perda

        Raises:
            UserError: Se o objeto 'self' são possuir move lines ref a baixa
                por perda.
        """
        # Dicionário para atualizar a linha principal da fatura
        main_update = {}
        # Obtém a account.move.line principal (a que possui a mesma conta da account.move)
        main_line = next((l for l in self.line_ids if l.account_id.id == self.account_id.id), None)  # noqa
        # Obtém as linhas que foram geradas na baixa por perda
        paid_loss_lines = self.line_ids.filtered(lambda line: line.loss_paid_move)

        if not paid_loss_lines:
            raise UserError("Nenhuma linha de baixa por perda foi encontrada. Apenas movimentações "\
                            "que tiveram linhas de baixa por perda podem ser estornadas por esse método.")
        if not main_line.debit:
            main_update.update({'debit': sum(paid_loss_lines.mapped('debit'))})

        if not main_line.credit:
            main_update.update({'credit': sum(paid_loss_lines.mapped('credit'))})

        # Valores para atualizar a linha principal da account.move
        lines_update = [(1, main_line.id, main_update)]

        # Gera linhas inversas as linhas geradas na baixa por perda
        for line in paid_loss_lines:
            vals = {
                'name': line.name + _(' (Reversal)'),
                'partner_id': line.partner_id.id,
                'date_maturity': line.date_maturity,
                'quantity': line.quantity,
                'account_id': line.account_id.id,
                'credit': line.debit,
                'debit': line.credit,
            }
            lines_update.append((0, 0, vals))
            line.loss_paid_move = False

        # Cancela e passa a account.move pro status 'draft'
        self.button_cancel()
        self.write({'line_ids': lines_update, 'paid_status': 'open'})

    @api.multi
    def action_make_title_in_negociation(self, values):
        for rec in self:
            rec.paid_status = 'in_negociation'

        return super(AccountMove, self).write(values)

    def action_make_title_back_to_open(self, values):
        for rec in self:
            rec.paid_status = 'open'

        return super(AccountMove, self).write(values)

    def cancel_title(self):
        """ Cancela título criando um registro contabil contrario, e gerando
            registro de conciliação com referencia nas duas movimentações.

        Returns:
            account.move -- Movimentação reversa de título (cancelamento)
        """
        for move in self:
            open_moves = move.filtered(lambda move: move.paid_status in ['open', 'discounted_title', 'cancelled'])

            if not open_moves:
                raise UserError(_('Apenas títulos sem pagamento podem ser cancelados!')) # noqa
            else:
                for record in open_moves:
                    amount_field = ('debit' if record.account_type == 'receivable' else 'credit') # noqa
                    counterpart_amls = [l for l in record.line_ids if l.account_id.id != record.account_id.id] # noqa
                    active_aml = next((l for l in record.line_ids if l.account_id.id == record.account_id.id), None) # noqa
                    values = [(1, active_aml.id if active_aml else False, {amount_field: 0})] # noqa

                    for line in counterpart_amls:
                        values.append((0, 0, {
                            'name': line.name,
                            'partner_id': line.partner_id.id,
                            'date_maturity': (
                                line.move_id.date_maturity_current),
                            'quantity': line.quantity,
                            'debit': line.credit,
                            'credit': line.debit,
                            'account_id': line.account_id.id,
                        }))

                    record.button_cancel()

                    record.paid_status = 'cancelled'

                    record.write({
                        'line_ids': values,
                    })

                    record.post()

    def adjust_payment_datetime(self):
        """Retorna a data da ultima baixa relacionada ao título, se o título
        possuir alguma baixa relacionada.
        """
        for rec in self:
            if rec.payment_ids:
                rec.payment_datetime = max(line.payment_date.strftime('%Y-%m-%d') for line in rec.payment_ids)
            else:
                rec.payment_datetime = False

    def adjust_payment_amount(self):
        """Retorna soma do valor de todas as baixas relacionadas ao título,
        se o título possuir alguma baixa relacionada
        """
        payments = [payment.amount for payment in self.payment_ids if payment.state not in ['draft', 'cancelled']] # noqa

        self.amount_payment_value = payments and sum(payments) or 0
