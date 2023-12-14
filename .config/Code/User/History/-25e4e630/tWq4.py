import re

from odoo import api, fields, models
from odoo.addons.rest_api_tdssolucoes_pdv.models.const import CODIGOS_PAGAMENTO
from odoo.exceptions import UserError

STATE = {'draft': [('readonly', False)]}


class PosOrderEntry(models.Model):
    _name = 'pos.order.entry'
    _description = 'Pos Order Entry'

    _rec_name = 'numero_venda'
    _order = 'write_date desc'

    config_guid = fields.Char(
        string='POS Config GUID',
        readonly=True,
        states=STATE,
    )

    session_guid = fields.Char(
        string='POS Session GUID',
        readonly=True,
        states=STATE,
    )

    numero_venda = fields.Char(
        string='Numero da Venda',
        readonly=True,
        states=STATE,
    )

    cliente_nome = fields.Char(
        string='Cliente',
        readonly=True,
        states=STATE,
    )

    cliente_cnpj_cpf = fields.Char(
        string='CNPJ/CPF',
        readonly=True,
        states=STATE,
    )

    cliente_endereco = fields.Char(
        string='Endereço',
        readonly=True,
        states=STATE,
    )

    valor_venda = fields.Char(
        string='Valor Venda',
        readonly=True,
        states=STATE,
    )

    valor_desconto = fields.Char(
        string='Valor Desconto',
        readonly=True,
        states=STATE,
    )

    valor_liquido = fields.Char(
        string='Valor Liquido',
        readonly=True,
        states=STATE,
    )

    tipo_pag_pdv = fields.Char(
        string='Tipo Pag. PDV',
        readonly=True,
        states=STATE,
    )

    pos_order_entry_line_ids = fields.One2many(
        comodel_name='pos.order.entry.line',
        inverse_name='pos_order_entry_id',
        string='Lines',
        readonly=True,
        states=STATE,
    )

    pos_order_entry_event_ids = fields.One2many(
        comodel_name='pos.order.entry.event',
        inverse_name='pos_order_entry_id',
        string='Events',
        readonly=True,
    )

    pos_order_id = fields.Many2one(
        comodel_name='pos.order',
        string='POS Order',
        readonly=True,
        states=STATE,
    )

    state = fields.Selection(
        selection=[
            ('draft', 'Provisório'),
            ('open', 'Aberto'),
            ('done', 'Finalizado'),
            ('error', 'Erro'),
            ('cancel', 'Cancelado'),
        ],
        string='State',
        default='draft',
        readonly=True,
        states=STATE
    )

    create_date = fields.Datetime(
        string='Create Date',
        readonly=True,
    )

    write_date = fields.Datetime(
        string='Write Date',
        readonly=True,
    )

    create_uid = fields.Many2one(
        'res.users',
        string='Create User ID',
        readonly=True,
    )

    write_uid = fields.Many2one(
        'res.users',
        string='Write User ID',
        readonly=True,
    )

    def _format_decimal_values(self, value):
        """Converte valores decimais com
        virgula com separador decimal para um formato
        que permite a conversão para float.

        Args:
            value (str): valor a ser formatado

        Returns:
            str: valor formatado
        """
        if not isinstance(value, str):
            return float(value)

        return float(value.replace('.', '').replace(',', '.'))

    @api.multi
    def unlink(self):
        """Sobrescreve metodo unlink para permitir
        exclusão apenas quando a registro estiver no status
        'error'

        Returns:
            boolean: Se a exclusao foi bem sucedidad_
        """

        for rec in self:
            if rec.state == 'done':
                raise UserError("Apenas registros com status diferente de 'Finalizado' podem ser excluídos.")

        return super(PosOrderEntry, self).unlink()

    @api.multi
    def action_back_to_draft(self):
        """Retorna status da entradas para provisório. O retorno
        funciona apenas para entradas com status 'Erro'.

        Raises:
            UserError: se o status da entrada for diferente de 'error'
        """

        for rec in self:

            if rec.state in ('open', 'error'):
                rec.write({'state': 'draft'})

            else:
                raise UserError('Somente requisições com status diferente de "Finalizado" podem retornar para Provisório')

    @api.multi
    def action_cancel_entry(self):
        """Cancela entrada. Entradas canceladas não são processadas.

        Raises:
            UserError: Se o status da entrada for diferente de 'Provisorio' ou 'Erro'
        """

        for rec in self:

            if rec.state in ('draft', 'error'):
                rec.state = 'cancel'
            else:
                raise UserError('Somente entradas com status "Provisório" ou "Erro" podem ser canceladas')

    @api.multi
    def action_confirm_entry(self):
        """Confirma entrada alterando seu status para 'Aberto'
        Desse modo o sistema pode converte-lo para POS Order.

        Raises:
            UserError: se o status da entrada for diferente de 'Provisorio'
        """
        for rec in self:

            if rec.state == 'draft':
                rec.state = 'open'
            else:
                raise UserError('Somente entradas com status "Provisório" podem ser confirmadas')

    @api.multi
    def action_convert_to_pos_order(self):
        """Converte entradas de requisição em registro do POS
        """

        POS_ORDER_ENTRY_EVENT = self.env['pos.order.entry.event']

        for rec in self:

            rec.state = 'error'

            pos_config = self.env['pos.config'].search([('guid', '=', rec.config_guid)], limit=1)

            if not pos_config:

                POS_ORDER_ENTRY_EVENT.create({
                    'category': 'error',
                    'name': f'POS Config: {rec.config_guid} não encontrado!',
                    'pos_order_entry_id': rec.id,
                })

                continue

            pos_session = self.env['pos.session'].search([('guid', '=', rec.session_guid)], limit=1)

            if not pos_session:

                POS_ORDER_ENTRY_EVENT.create({
                    'category': 'error',
                    'name': f'POS Session: {rec.session_guid} não encontrado',
                    'pos_order_entry_id': rec.id,
                })

                continue

            lines = []

            for item in rec.pos_order_entry_line_ids:

                product = self.env['product.product'].search([('default_code', '=', item.codigo_produto)])

                if not product:

                    POS_ORDER_ENTRY_EVENT.create({
                        'category': 'error',
                        'name': f'Produto de código: {item.codigo_produto} não encontrado',
                        'pos_order_entry_id': rec.id,
                    })

                    continue

                try:

                    lines.append((0, 0, {
                        'qty': item.quantidade or 0,
                        'price_unit': self._format_decimal_values(item.preco) or 0,
                        'price_subtotal': self._format_decimal_values(item.preco) or 0,
                        'price_subtotal_incl': self._format_decimal_values(item.total_liquido) or 0,
                        'discount': self._format_decimal_values(item.desconto) or 0,
                        'product_id': product.id,
                    }))

                except TypeError as exc:

                    POS_ORDER_ENTRY_EVENT.create({
                        'category': 'error',
                        'name': f'Erro na conversão de valors do item: {exc}',
                        'pos_order_entry_id': rec.id,
                    })

                    continue

            # Se ocorrer algum erro no cadastro da linhas, a quantidade de
            # itens não vai coincidir com a quantidade de linhas do POS Order
            if len(lines) != len(rec.pos_order_entry_line_ids):

                POS_ORDER_ENTRY_EVENT.create({
                    'category': 'error',
                    'name': 'Alguns itens não foram convertidos.',
                    'pos_order_entry_id': rec.id,
                })

                continue

            # remove pontos e/ou tracos do cnpj ou cpf
            val = re.sub('[^0-9]', '', rec.cliente_cnpj_cpf)

            if len(val) == 14:
                cnpj_cpf = f"{val[0:2]}.{val[2:5]}.{val[5:8]}/{val[8:12]}-{val[12:14]}"
            else:
                cnpj_cpf = f"{val[0:3]}.{val[3:6]}.{val[6:9]}-{val[9:11]}"

            if cnpj_cpf:
                partner = self.env['res.partner'].search([('cnpj_cpf', '=', cnpj_cpf)]) or False
            else:
                partner = None

            # Se nao encontrar o partner, tentamos cadastra-lo no sistema
            if not partner and cnpj_cpf and rec.cliente_nome:

                partner = self.env['res.partner'].create({
                    'name': rec.cliente_nome,
                    'cnpj_cpf': cnpj_cpf,
                    'street': rec.cliente_endereco,
                })

                # formatamos o cnpj
                partner.onchange_cnpj_cpf()

                POS_ORDER_ENTRY_EVENT.create({
                    'category': 'info',
                    'name': f'Parceiro {rec.cliente_nome} cadastrado',
                    'pos_order_entry_id': rec.id,
                })

            # verificamos se o codigo do tipo de pagamento esta correto
            if rec.tipo_pag_pdv not in CODIGOS_PAGAMENTO:

                POS_ORDER_ENTRY_EVENT.create({
                    'category': 'error',
                    'name': f'Tipo de Pagamento {rec.tipo_pag_pdv} inválido.',
                    'pos_order_entry_id': rec.id,
                })

                continue

            # verificamos se o codigo do tipo de pagamento esta correto
            if rec.tipo_pag_pdv not in CODIGOS_PAGAMENTO:

                POS_ORDER_ENTRY_EVENT.create({
                    'category': 'error',
                    'name': f'Tipo de Pagamento {rec.tipo_pag_pdv} inválido.',
                    'pos_order_entry_id': rec.id,
                })

                continue

            # verificamos se o codigo do tipo de pagamento esta correto
            if rec.tipo_pag_pdv not in CODIGOS_PAGAMENTO:

                POS_ORDER_ENTRY_EVENT.create({
                    'category': 'error',
                    'name': f'Tipo de Pagamento {rec.tipo_pag_pdv} inválido.',
                    'pos_order_entry_id': rec.id,
                })

                continue

            # verificamos se o codigo do tipo de pagamento esta correto
            if rec.tipo_pag_pdv not in CODIGOS_PAGAMENTO:

                POS_ORDER_ENTRY_EVENT.create({
                    'category': 'error',
                    'name': f'Tipo de Pagamento {rec.tipo_pag_pdv} inválido.',
                    'pos_order_entry_id': rec.id,
                })

                continue
            vals = {
                'session_id': pos_session.id,
                'fiscal_position_id': pos_config.default_fiscal_position_id.id,
                'total_bruto': self._format_decimal_values(rec.valor_venda),
                'total_desconto': self._format_decimal_values(rec.valor_desconto),
                'amount_total': self._format_decimal_values(rec.valor_liquido),
                'amount_paid': 0,
                'amount_tax': 0,
                'amount_return': 0,
                'lines': lines,
                'pricelist_id': pos_config.pricelist_id.id,
                'location_id': pos_config.stock_location_id.id,
                'order_from_pdv': True,
                'tipo_pag_pdv': rec.tipo_pag_pdv,
                'partner_id': partner.id if partner else False,
                'company_id': pos_config.company_id.id,
            }

            order = self.env['pos.order'].create(vals)

            order.write({
                'name': rec.numero_venda,
                'location_id': pos_config.stock_location_id.id,
            })

            rec.write({
                'state': 'done',
                'pos_order_id': order.id,
            })

            POS_ORDER_ENTRY_EVENT.create({
                'category': 'info',
                'name': 'Entrada convertida em pedido do POS com sucesso',
                'pos_order_entry_id': rec.id,
            })

    @api.multi
    def cron_convert_pos_order_entry(self):
        """Envia todas as entradas para que sejam processadas
        e convertidas para pedidos do POS.
        """

        entries = self.env['pos.order.entry'].search(
            domain=[('state', '=', 'open')],
        )

        # enviamos as entradas para a fila para que cada uma delas
        # seja processada separadamente
        for entry in entries:
            entry.with_delay().action_convert_pos_order_entry()

            self.env['pos.order.entry.event'].create({
                'category': 'info',
                'name': 'Entrada na fila para conversão em pedido do POS',
                'pos_order_entry_id': entry.id,
            })
