import base64
import datetime
import json
import re

from odoo import http
from odoo.addons.muk_rest import tools
from odoo.addons.muk_rest.tools.json import ResponseEncoder
from odoo.addons.rest_api_tdssolucoes_pdv.models.const import CODIGOS_PAGAMENTO
from odoo.http import Response, request

# Nomes para os campos que devem ser retornados com o produto
# Foram utilizados constantes para que a alteracao do
# nome do campo retornado seja realizado apenas aqui, caso
# seja necessario
ID = 'id'
CODIGO = 'codigo'
DESCRICAO = 'descricao'
UNIDADE = 'unidade'
NCM = 'ncm'
CEST = 'cest'
ORIGEM = 'origem'
EMPRESA = 'empresa'

CFOP = 'cfop'
ICMS_ALIQUOTA = 'icms_aliquota'
ICMS_CST = 'icms_cst'
PIS_CST = 'pis_cst'
CONFINS_CST = 'confins_cst'
LEI_TRANSPARENCIA = 'lei_transparencia'


REQUIRED_SALE_FIELDS = [
    'config_guid',
    'session_guid',
    'numero_venda',
    'valor_venda',
    'valor_desconto',
    'valor_liquido',
    'tipo_pagamento',
]

REQUIRED_SALE_ITEM_FIELDS = [
    'quantidade',
    'preco',
    'desconto',
    'total_liquido',
    'codigo_produto',
]


class Channel(http.Controller):

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
            return value

        return value.replace('.', '').replace(',', '.')

    def _create_attachment(self, prefix, pos_order, data):
        """Anexa json ao pos.order.

        Args:
            prefix (str): prefixo utilizado no nome do arquivo anexo
            pos_order (por.order): pedido onde o json sera anexado
            data (dict): dados do json a serem salvos em anexo
        """

        request_body = {
            'numero_venda': data['numero_venda'],
            'valor_venda': data['valor_venda'],
            'valor_desconto': data['valor_desconto'],
            'valor_liquido': data['valor_liquido'],
            'cpf_cnpj': data['cpf_cnpj'],
            'cliente': data['cliente'],
            'endereco': data['endereco'],
            'tipo_pagamento': data['tipo_pagamento'],
            'items': json.loads(data['items']),
            'token': data['token'].access_token,
            'oauth': data['oauth'].name,
            'config_guid': data['config_guid'],
            'session_guid': data['session_guid'],
            'custom': data['custom'],
        }

        request_json = json.dumps(
            request_body, indent=2, cls=ResponseEncoder)

        file_name = f'{prefix}-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")}.json'

        request.env['ir.attachment'].create({
            'name': file_name,
            'datas': base64.b64encode(request_json.encode()),
            'datas_fname': file_name,
            'description': '',
            'res_model': 'pos.order',
            'res_id': pos_order.id,
        })

    def _get_extra_products_info(self, config_guid, ctx):
        """Retorna informações extras do produto relacionada
        a impostos da pos. fiscal

        Args:
            config_guid (char): o guid da pos.config utilizada
            ctx (dict): contexto criado na requisição

        Returns:
            dict: dicionario com as informações do produto
        """

        extra_product_data = {
            CFOP: '',
            ICMS_ALIQUOTA: '',
            ICMS_CST: '',
            PIS_CST: '',
            CONFINS_CST: '',
            LEI_TRANSPARENCIA: '',
        }

        if not config_guid:
            return extra_product_data

        pos_config = request.env['pos.config'].with_context(ctx).search([('guid', '=', config_guid)], limit=1)  # noqa

        if pos_config:

            icms_rules = pos_config.default_fiscal_position_id.icms_tax_rule_ids
            pis_rules = pos_config.default_fiscal_position_id.pis_tax_rule_ids
            cofins_rules = pos_config.default_fiscal_position_id.cofins_tax_rule_ids

            if icms_rules:

                icms = icms_rules[0]

                extra_product_data[CFOP] = icms.cfop_id.code if icms.cfop_id else ''
                extra_product_data[ICMS_CST] = icms.cst_icms or ''
                extra_product_data[ICMS_ALIQUOTA] = icms.tax_id.amount if icms.tax_id else 0.0

            if pis_rules:
                extra_product_data[PIS_CST] = pis_rules[0].cst_pis or ''

            if cofins_rules:
                extra_product_data[CONFINS_CST] = cofins_rules[0].cst_cofins or ''

        return extra_product_data

    @http.route([
        '/api/pdv/produtos',
        '/api/pdv/produtos/<string:codigo_produto>',
        '/api/pdv/produtos/<string:guid>',
        '/api/pdv/produtos/<string:cnpjcpf>',
    ], auth="none", type='http', methods=['GET'], csrf=False)
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected()
    def get_pdv_produtos(self, codigo_produto=None, guid=None, cnpjcpf=None, context=None, **kw):
        """Método GET para a model 'product.product'.

        Keyword Arguments:
            codigo_produto {str} -- Referência Interna do Projeto a ser retornado (default: {None})
            guid {str} -- GUID da config. do POS que sera usada para calculos os impostos (default: {None})
            cnpjcpf {str} -- CNPJ/CPF para buscar os produtos de uma determinada empresa (default: {None})
            context {dict} -- Variavel 'context' para envio de valores adicionais (default: {None})

        Returns:
            dict -- Resposta do GET no formato JSON
        """

        # Guid da configuracao do POS que possui a Pos. Fiscal que sera usada no
        # calculo dos impostos
        config_guid = guid

        ctx = request.session.context.copy()
        ctx.update(context and json.loads(context) or {})

        if codigo_produto:
            domain = [('default_code', '=', codigo_produto)]

        elif cnpjcpf:

            company = request.env['res.company'].with_context(ctx).search([('cnpj_cpf', '=', json.loads(cnpjcpf))], limit=1)  # noqa
            domain = [('company_id', '=', company.id)]

        else:
            domain = []

        if config_guid:
            # Busca dados adicionais do produto a partir do pos.config
            extra_product_data = self._get_extra_products_info(config_guid=config_guid, ctx=ctx)  # noqa

        else:
            extra_product_data = {}

        domain += [
            ('sale_ok', '=', True),
            ('fiscal_type', '=', 'product'),
            ('type', 'in', ['consu', 'product']),
        ]

        products = request.env['product.product'].with_context(ctx).search(domain)  # noqa

        response = []

        for prod in products:

            ncm = ''
            federal = ''

            if prod.fiscal_classification_id:

                ncm = prod.fiscal_classification_id.code or ''

                if prod.origin:

                    if prod.origin in ('1', '2', '3', '8'):
                        federal = prod.fiscal_classification_id.federal_nacional or 0.0
                    else:
                        federal = prod.fiscal_classification_id.federal_importado or 0.0

            response.append({
                ID: prod.id,
                CODIGO: prod.default_code or '',
                DESCRICAO: prod.name,
                UNIDADE: prod.uom_id.name if prod.uom_id else '',
                CEST: prod.cest or '',
                NCM: ncm or '',
                ORIGEM: prod.origin or '',
                EMPRESA: prod.company_id.name if prod.company_id else '',
                LEI_TRANSPARENCIA: federal,
                **extra_product_data,
            })

        # Build content os HTTP response
        response_json = json.dumps(response, sort_keys=False, indent=4, cls=ResponseEncoder)  # noqa

        return Response(response_json, content_type='application/json;charset=utf-8', status=200)

    @http.route([
        '/api/pdv/vendas',
    ], auth="none", type='http', methods=['POST'], csrf=False)
    @tools.common.parse_exception
    @tools.common.ensure_database
    @tools.common.ensure_module()
    @tools.security.protected(operations=['create'])
    def post_pdv_venda(self, context=None, **kw):
        """Método POST para gravação dos dados de venda do PDV

        Keyword Arguments:
            context {dict} -- Variavel 'context' para envio de valores adicionais (default: {None})

        Returns:
            dict -- Resposta do POST contendo ID do Pedido Criado e mensagem de sucesso, ou mensagem de erro em caso de falha.
        """

        ctx = request.session.context.copy()
        ctx.update(context and json.loads(context) or {})

        values = kw

        # Verificamos se os campos obrigatorios estao presentes
        if not all([(field in values) and field for field in REQUIRED_SALE_FIELDS]):

            result = {
                'message': 'Campos obrigatórios não encontrados!',
            }

            return Response(json.dumps(result, indent=4, cls=ResponseEncoder),
                            content_type='application/json;charset=utf-8',
                            status=400)

        if request.env['pos.order'].with_context(ctx).search([('name', '=', values['numero_venda'].strip())]):

            # o numero da venda deve ser unico
            result = {
                'message': f'Venda {values["numero_venda"]} já registrada no sistema.',
            }

            return Response(json.dumps(result, indent=4, cls=ResponseEncoder),
                            content_type='application/json;charset=utf-8',
                            status=200)

        if values['tipo_pagamento'] not in CODIGOS_PAGAMENTO:

            # o numero da venda deve ser unico
            result = {
                'message': f'Tipo de Pagamento {values["tipo_pagamento"]} inválido.',
            }

            return Response(json.dumps(result, indent=4, cls=ResponseEncoder),
                            content_type='application/json;charset=utf-8',
                            status=400)

        try:

            pos_config = request.env['pos.config'].with_context(ctx).search([('guid', '=', values['config_guid'])], limit=1)  # noqa
            pos_session = request.env['pos.session'].with_context(ctx).search([('guid', '=', values['session_guid'])], limit=1)  # noqa

            lines = []

            for item in json.loads(values['items']):

                product = request.env['product.product'].with_context(ctx).search([('default_code', '=', item['codigo_produto'])])  # noqa

                if not product:

                    # producao nao localizado
                    result = {
                        'message': f'Venda {values["numero_venda"]}: Produto com código {item["codigo_produto"]} não encontrado.',
                    }

                    content = json.dumps(result, indent=4, cls=ResponseEncoder)

                    return Response(content,
                                    content_type='application/json;charset=utf-8',
                                    status=404)

                lines.append((0, 0, {
                    'qty': item['quantidade'],
                    'price_unit': self._format_decimal_values(item['preco']),
                    'price_subtotal': self._format_decimal_values(item['preco']),
                    'price_subtotal_incl': self._format_decimal_values(item['total_liquido']),
                    'discount': self._format_decimal_values(item['desconto']),
                    'product_id': product.id,
                }))

            vals = {
                'session_id': pos_session.id,
                'fiscal_position_id': pos_config.default_fiscal_position_id.id,
                'total_bruto': self._format_decimal_values(values['valor_venda']),
                'total_desconto': self._format_decimal_values(values['valor_desconto']),
                'amount_total': self._format_decimal_values(values['valor_liquido']),
                'amount_paid': 0,
                'amount_tax': 0,
                'amount_return': 0,
                'lines': lines,
                'pricelist_id': pos_config.pricelist_id.id,
                'location_id': pos_config.stock_location_id.id,
                'order_from_pdv': True,
                'tipo_pag_pdv': values['tipo_pagamento'],
            }

            # remove pontos e/ou tracos do cnpj ou cpf
            val = re.sub('[^0-9]', '', values.get('cpf_cnpj', ''))

            if len(val) == 14:
                cnpj_cpf = f"{val[0:2]}.{val[2:5]}.{val[5:8]}/{val[8:12]}-{val[12:14]}"
            else:
                cnpj_cpf = f"{val[0:3]}.{val[3:6]}.{val[6:9]}-{val[9:11]}"

            if cnpj_cpf:
                partner = request.env['res.partner'].search(domain) or False  # noqa
            else:
                partner = None

            name = values.get('cliente', None)

            # Se nao encontrar o partner, tentamos cadastra-lo no sistema
            if not partner and cnpj_cpf and name:

                partner = request.env['res.partner'].create({
                    'name': name,
                    'cnpj_cpf': cnpj_cpf,
                })

                # formatamos o cnpj
                partner.onchange_cnpj_cpf()

            vals['partner_id'] = partner.id

            rec = request.env['pos.order'].with_context(ctx).create(vals)

            rec.write({
                'name': values['numero_venda'],
                'location_id': pos_config.stock_location_id.id,
            })

            response = {
                'ID': rec.id,
                'numero_venda': rec.name,
                'message': 'Cadastro efetuado com sucesso',
            }

            content = json.dumps(response, indent=4, cls=ResponseEncoder)

            # salvamos o conteudo da requisicao
            self._create_attachment('pdv-venda', rec, kw)

            return Response(content, content_type='application/json;charset=utf-8', status=200)  # noqa

        except Exception as exc:

            result = {
                'message': str(exc),
            }

            return Response(json.dumps(result, indent=4, cls=ResponseEncoder),
                            content_type='application/json;charset=utf-8',
                            status=400)
