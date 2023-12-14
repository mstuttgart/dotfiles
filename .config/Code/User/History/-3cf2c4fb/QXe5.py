import os
import base64
import logging
import mock
import urllib3
import requests

from odoo import fields
from odoo.addons.br_account.tests.test_base import TestBaseBr

_logger = logging.getLogger(__name__)

try:
    from pytrustnfe.xml import sanitize_response
except ImportError:
    _logger.debug('Cannot import pytrustnfe')


class TestNFeDSF(TestBaseBr):
    caminho = os.path.dirname(__file__)

    def setUp(self):
        super(TestNFeDSF, self).setUp()

        self.main_company = self.env.ref('base.main_company')
        self.currency_real = self.env.ref('base.BRL')

        with open(os.path.join(self.caminho, 'teste.pfx'), 'rb') as f:
            nfe_a1_file = f.read()

        self.report = self.env.ref(
            'br_nfse_ginfes.report_br_nfse_danfe_sao_caetano')

        self.cnae = self.env.ref('br_data_account.l10n_br_cnae_2323')

        self.main_company.write({
            'name': 'MultidadosTI',
            'legal_name': 'MULTIDADOS INFORMATICA LTDA - EPP',
            'cnpj_cpf': '57.371.593/0001-10',
            'zip': '88037-240',
            'street': 'Vinicius de Moraes',
            'number': '42',
            'district': 'Centro',
            'country_id': self.env.ref('base.br').id,
            'state_id': self.env.ref('base.state_br_sp').id,
            'city_id': self.env.ref('br_base.city_3509502').id,
            'phone': '(11) 9999-8888',
            'inscr_mun': '51212300',
            'tipo_ambiente_nfse': '1',  # producao
            'webservice_nfse': 'nfse_ginfes',
            'report_nfse_id': self.report.id,
            'cnae_main_id': self.cnae.id,
            'nfe_a1_password': '123456',
            'nfe_a1_file': base64.b64encode(nfe_a1_file),
            'nfse_ginfes_regime_tributacao': '2',
            'nfse_ginfes_incentivador_cultural': '2',
        })

        if not self.main_company.currency_id:
            self.main_companu.currency_id = self.currency_real

        self.service_type = self.env.ref('br_data_account.service_type_101')

        self.service_type.codigo_tributacao_municipio = '3360500'

        self.title_type = self.env.ref('br_account.account_title_type_2')
        self.financial_operation = self.env.ref('br_account.account_financial_operation_6')  # noqa

        payment_term = self.env.ref('account.account_payment_term_net')

        self.service = self.env['product.product'].create({
            'name': 'Normal Service',
            'default_code': '25',
            'type': 'service',
            'fiscal_type': 'service',
            'list_price': 50.0,
        })

        self.partner_juridica = self.env['res.partner'].create({
            'name': 'Nome Parceiro',
            'legal_name': 'Razão Social',
            'zip': '88037-240',
            'street': 'Endereço Rua',
            'number': '42',
            'district': 'Centro',
            'phone': '(48) 9801-6226',
            'property_account_receivable_id': self.receivable_account.id,
            'cnpj_cpf': '05.075.837/0001-13',
            'company_type': 'company',
            'is_company': True,
            'inscr_est': '433.992.727',
            'country_id': self.env.ref('base.br').id,
            'state_id': self.env.ref('base.state_br_sc').id,
            'city_id': self.env.ref('br_base.city_4205407').id,
        })

        self.journalrec = self.env['account.journal'].create({
            'name': 'Faturas',
            'code': 'INV',
            'type': 'sale',
            'default_debit_account_id': self.revenue_account.id,
            'default_credit_account_id': self.revenue_account.id,
        })

        self.fpos = self.env['account.fiscal.position'].create({
            'name': 'Servico',
            'fiscal_document_id': self.env.ref('br_nfse.fiscal_document_001').id,  # noqa
            'document_serie_id': self.env.ref('br_nfse.br_document_serie_1').id,  # noqa
            'service_type_id': self.service_type.id,
            'position_type': 'service',
            'send_invoice_on': 'on_confirm',
            'nfse_ginfes_tipo_rps': '1',
            'nfse_ginfes_natureza_operacao': '2',
        })

        invoice_line_data = [
            (0, 0,
             {
                 'product_id': self.service.id,
                 'quantity': 10.0,
                 'account_id': self.revenue_account.id,
                 'name': 'product test 5',
                 'price_unit': 100.00,
                 'product_type': self.service.fiscal_type,
                 'cfop_id': self.env.ref('br_data_account_product.cfop_5101').id,  # noqa
                 'pis_cst': '01',
                 'cofins_cst': '01',
                 'tax_inss_id': self.inss_11.id,
                 'tax_issqn_id': self.issqn_500.id,
             }
             )
        ]

        self.invoices = self.env['account.invoice'].create({
            'name': 'Teste Validação',
            'fiscal_document_id': self.env.ref('br_nfse.fiscal_document_001').id,
            'document_serie_id': self.env.ref('br_nfse.br_document_serie_1').id,
            'journal_id': self.journalrec.id,
            'account_id': self.receivable_account.id,
            'fiscal_position_id': self.fpos.id,
            'invoice_line_ids': invoice_line_data,
            'webservice_nfse': 'nfse_ginfes',
            'payment_term_id': payment_term.id,
            'partner_id': self.partner_juridica.id,
            'state': 'draft',
        })

    def test_check_invoice_electronic_values(self):

        for invoice in self.invoices:

            # Cria parcelas
            invoice.generate_parcel_entry(self.financial_operation,
                                          self.title_type)

            # Confirmando plit
            # 'fatura deve gerar um documento eletrônico
            invoice.action_br_account_invoice_open()

            elec_inv = self.env['invoice.electronic'].search(
                [('invoice_id', '=', invoice.id)])

            self.assertEqual(elec_inv.nfse_ginfes_tipo_rps,
                             invoice.fiscal_position_id.nfse_ginfes_tipo_rps)

            self.assertEqual(elec_inv.nfse_ginfes_natureza_operacao,
                             invoice.fiscal_position_id.nfse_ginfes_natureza_operacao)

            self.assertEqual(elec_inv.nfse_ginfes_regime_tributacao,
                             elec_inv.company_id.nfse_ginfes_regime_tributacao)

            self.assertEqual(elec_inv.nfse_ginfes_incentivador_cultural,
                             elec_inv.company_id.nfse_ginfes_incentivador_cultural)

    @mock.patch('pytrustnfe.nfse.ginfes.cancelar_nfse')
    @mock.patch('pytrustnfe.nfse.ginfes.consultar_lote_rps')
    @mock.patch('pytrustnfe.nfse.ginfes.consultar_situacao_lote')
    @mock.patch('pytrustnfe.nfse.ginfes.recepcionar_lote_rps')
    def test_nfse_homologacao_sucesso(self, recepcionar_lote_rps, consultar_situacao_lote, consultar_lote_rps, cancelar_nfse):

        for invoice in self.invoices:

            # Cria parcelas
            invoice.generate_parcel_entry(self.financial_operation,
                                          self.title_type)

            # Confirmando a fatura deve gerar um documento eletrônico
            invoice.action_br_account_invoice_open()

            # Lote recebido com sucesso
            with open(os.path.join(self.caminho, 'xml', 'enviar_lote_rps_resposta.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            resp = sanitize_response(xml_recebido)

            recepcionar_lote_rps.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            elec_inv = self.env['invoice.electronic'].search(
                [('invoice_id', '=', invoice.id)])

            elec_inv.action_send_electronic_invoice()

            # envio inicial do arquivo
            self.assertEqual(elec_inv.state, 'open')
            self.assertEqual(elec_inv.recibo_nfe, '515054802')

            # NOTE: Testa status 'na fila de processamento'
            # -------------------------------------------

            # Consulta do resultado do lote
            with open(os.path.join(self.caminho, 'xml', 'consultar_situacao_rps_resposta_2.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            # testa status de retorno 2
            resp = sanitize_response(xml_recebido)

            consultar_situacao_lote.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            elec_inv.action_get_electronic_invoice_status()

            self.assertEqual(elec_inv.state, 'open')
            self.assertEqual(elec_inv.codigo_retorno, '2')
            self.assertEqual(elec_inv.mensagem_retorno, 'Lote aguardando processamento')

            events = elec_inv.electronic_event_ids

            self.assertEqual(len(events), 1)
            self.assertEqual(events.code, '2')
            self.assertEqual(events.name, elec_inv.mensagem_retorno)
            self.assertEqual(events.category, 'info')

            # NOTE: Testa status 'processado com sucesso'
            # -------------------------------------------

            # Consulta do resultado do lote
            with open(os.path.join(self.caminho, 'xml', 'consultar_situacao_rps_resposta_4.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            # testa status de retorno 4
            resp = sanitize_response(xml_recebido)

            consultar_situacao_lote.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            # Realizamos o mock do metodo 'consultar_situacao_lote'
            # de modo a simular o ginfes retornando os dados de sucesso da nfse
            # Consulta do resultado do lote
            with open(os.path.join(self.caminho, 'xml', 'consultar_lote_rps_resposta.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            resp = sanitize_response(xml_recebido)

            consultar_lote_rps.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            elec_inv.action_get_electronic_invoice_status()

            dt = fields.Date.context_today(elec_inv)

            self.assertEqual(elec_inv.state, 'done')
            self.assertEqual(elec_inv.codigo_retorno, '100')
            self.assertEqual(elec_inv.mensagem_retorno, 'NFSe emitida com sucesso')
            self.assertEqual(elec_inv.numero, 1070)

            self.assertEqual(elec_inv.invoice_id.date_invoice, dt)
            self.assertEqual(elec_inv.invoice_id.internal_number, 1070)
            self.assertEqual(elec_inv.verify_code, 'XPTOXPTO')

            # o numero do lote e gerado pelo sistema
            self.assertEqual(elec_inv.lote_code, str(elec_inv.id))
            self.assertEqual(elec_inv.data_autorizacao,
                             fields.Date.to_string(dt))

            events = elec_inv.electronic_event_ids

            self.assertEqual(len(events), 2)
            self.assertEqual(events[0].code, '100')
            self.assertEqual(events[0].name, 'NFSe emitida com sucesso')
            self.assertEqual(events[0].category, 'info')

            # Consulta do resultado do lote
            with open(os.path.join(self.caminho, 'xml', 'cancelar_nfse_resposta.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            resp = sanitize_response(xml_recebido)

            cancelar_nfse.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            # Cancelamento da NFSe
            elec_inv.action_cancel_document()

            self.assertEqual(elec_inv.state, 'cancel')
            self.assertEqual(elec_inv.codigo_retorno, '100')
            self.assertEqual(elec_inv.mensagem_retorno,
                             'Nota Fiscal de Serviço Cancelada')

            events = elec_inv.electronic_event_ids

            self.assertEqual(len(events), 3)

            self.assertEqual(events[0].code, '100')
            self.assertEqual(events[0].name, elec_inv.mensagem_retorno)
            self.assertEqual(events[0].category, 'info')

    @mock.patch('pytrustnfe.nfse.ginfes.consultar_situacao_lote')
    @mock.patch('pytrustnfe.nfse.ginfes.recepcionar_lote_rps')
    def test_nfse_consultar_situacao_lote_erro(self, recepcionar_lote_rps, consultar_situacao_lote):

        for invoice in self.invoices:

            # Cria parcelas
            invoice.generate_parcel_entry(self.financial_operation,
                                          self.title_type)

            # Confirmando a fatura deve gerar um documento eletrônico
            invoice.action_br_account_invoice_open()

            # Lote recebido com sucesso
            with open(os.path.join(self.caminho, 'xml', 'enviar_lote_rps_resposta.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            resp = sanitize_response(xml_recebido)

            recepcionar_lote_rps.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            elec_inv = self.env['invoice.electronic'].search(
                [('invoice_id', '=', invoice.id)])

            elec_inv.action_send_electronic_invoice()

            # envio inicial do arquivo
            self.assertEqual(elec_inv.state, 'open')
            self.assertEqual(elec_inv.recibo_nfe, '515054802')

            # NOTE: Testa status 'aguardando envio'
            # -------------------------------------------

            # Consulta do resultado do lote
            with open(os.path.join(self.caminho, 'xml', 'consultar_situacao_rps_resposta_1.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            # testa status de retorno 1
            resp = sanitize_response(xml_recebido)

            consultar_situacao_lote.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            elec_inv.action_get_electronic_invoice_status()

            self.assertEqual(elec_inv.state, 'draft')
            self.assertEqual(elec_inv.codigo_retorno, '1')
            self.assertEqual(elec_inv.mensagem_retorno, 'Aguardando envio')

    @mock.patch('pytrustnfe.nfse.ginfes.consultar_lote_rps')
    @mock.patch('pytrustnfe.nfse.ginfes.consultar_situacao_lote')
    @mock.patch('pytrustnfe.nfse.ginfes.recepcionar_lote_rps')
    def test_nfse_consulta_lote_rps_erro(self, recepcionar_lote_rps, consultar_situacao_lote, consultar_lote_rps):

        for invoice in self.invoices:

            # Cria parcelas
            invoice.generate_parcel_entry(self.financial_operation,
                                          self.title_type)

            # Confirmando a fatura deve gerar um documento eletrônico
            invoice.action_br_account_invoice_open()

            # Lote recebido com sucesso
            with open(os.path.join(self.caminho, 'xml', 'enviar_lote_rps_resposta.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            resp = sanitize_response(xml_recebido)

            recepcionar_lote_rps.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            elec_inv = self.env['invoice.electronic'].search(
                [('invoice_id', '=', invoice.id)])

            elec_inv.action_send_electronic_invoice()

            # envio inicial do arquivo
            self.assertEqual(elec_inv.state, 'open')
            self.assertEqual(elec_inv.recibo_nfe, '515054802')

            # NOTE: Testa status 'processado com erro'
            # -------------------------------------------

            # Consulta do resultado do lote
            with open(os.path.join(self.caminho, 'xml', 'consultar_situacao_rps_resposta_3.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            # testa status de retorno 3
            resp = sanitize_response(xml_recebido)

            consultar_situacao_lote.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            # Realizamos o mock do metodo 'consultar_situacao_lote'
            # de modo a simular o ginfes retornando os dados de erro
            # Consulta do resultado do lote
            with open(os.path.join(self.caminho, 'xml', 'consultar_lote_rps_resposta_erro.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            resp = sanitize_response(xml_recebido)

            consultar_lote_rps.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            elec_inv.action_get_electronic_invoice_status()

            self.assertEqual(elec_inv.state, 'error')
            self.assertEqual(elec_inv.codigo_retorno, 'E181')
            self.assertEqual(elec_inv.mensagem_retorno, 'Valor líquido de NFSe informada incorretamente')
            events = elec_inv.electronic_event_ids

            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].code, 'E181')
            self.assertEqual(events[0].name, 'Valor líquido de NFSe informada incorretamente')
            self.assertEqual(events[0].category, 'info')

    @mock.patch('pytrustnfe.nfse.ginfes.consultar_nfse_por_rps')
    @mock.patch('pytrustnfe.nfse.ginfes.consultar_lote_rps')
    @mock.patch('pytrustnfe.nfse.ginfes.consultar_situacao_lote')
    @mock.patch('pytrustnfe.nfse.ginfes.recepcionar_lote_rps')
    def test_nfse_consulta_lote_rps_erro_E10(self, recepcionar_lote_rps, consultar_situacao_lote, consultar_lote_rps, consultar_nfse_por_rps):

        for invoice in self.invoices:

            # Cria parcelas
            invoice.generate_parcel_entry(self.financial_operation,
                                          self.title_type)

            # Confirmando a fatura deve gerar um documento eletrônico
            invoice.action_br_account_invoice_open()

            # Lote recebido com sucesso
            with open(os.path.join(self.caminho, 'xml', 'enviar_lote_rps_resposta.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            resp = sanitize_response(xml_recebido)

            recepcionar_lote_rps.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            elec_inv = self.env['invoice.electronic'].search(
                [('invoice_id', '=', invoice.id)])

            elec_inv.action_send_electronic_invoice()

            # envio inicial do arquivo
            self.assertEqual(elec_inv.state, 'open')
            self.assertEqual(elec_inv.recibo_nfe, '515054802')

            # NOTE: Testa status 'processado com erro'
            # -------------------------------------------

            # Realizamos o mock do metodo 'consultar_situacao_lote'
            with open(os.path.join(self.caminho, 'xml', 'consultar_situacao_rps_resposta_3.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            # testa status de retorno 3
            resp = sanitize_response(xml_recebido)

            consultar_situacao_lote.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            # Realizamos o mock do metodo 'consultar_lote_rps'
            with open(os.path.join(self.caminho, 'xml', 'consultar_lote_rps_resposta_erro_E10.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            resp = sanitize_response(xml_recebido)

            consultar_lote_rps.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            # Realizamos o mock do metodo 'consultar_lote_rps'
            with open(os.path.join(self.caminho, 'xml', 'consultar_nfse_por_rps_resposta_erro_E10.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            resp = sanitize_response(xml_recebido)

            consultar_nfse_por_rps.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            elec_inv.action_get_electronic_invoice_status()

            self.assertEqual(elec_inv.state, 'done')
            self.assertEqual(elec_inv.codigo_retorno, '100')
            self.assertEqual(elec_inv.mensagem_retorno, 'Nota Fiscal emitida com sucesso')
            self.assertEqual(elec_inv.numero, 1010)
            self.assertEqual(elec_inv.invoice_id.internal_number, 1010)
            self.assertEqual(elec_inv.verify_code, 'XPTOXPTO')
            self.assertEqual(elec_inv.data_autorizacao, '2023-06-02T11:02:27')

            events = elec_inv.electronic_event_ids

            self.assertEqual(len(events), 2)

    @mock.patch('pytrustnfe.nfse.ginfes.recepcionar_lote_rps')
    def test_nfse_timeout_error_recepcionar_lote_rps(self, recepcionar_lote_rps):

        for invoice in self.invoices:

            # Cria parcelas
            invoice.generate_parcel_entry(self.financial_operation,
                                          self.title_type)

            # Confirmando a fatura deve gerar um documento eletrônico
            invoice.action_br_account_invoice_open()

            recepcionar_lote_rps.side_effect = urllib3.exceptions.MaxRetryError(
                mock.Mock(), '')

            invoice_electronic = self.env['invoice.electronic'].search(
                [('invoice_id', '=', invoice.id)])

            invoice_electronic.action_send_electronic_invoice()

            self.assertEqual(invoice_electronic.state, 'draft')
            self.assertEqual(invoice_electronic.codigo_retorno, 'TIMEOUT')
            self.assertTrue(invoice_electronic.mensagem_retorno)

            events = invoice_electronic.electronic_event_ids

            self.assertEqual(len(events), 1)
            self.assertEqual(events.code, 'TIMEOUT')
            self.assertEqual(events.name, invoice_electronic.mensagem_retorno)
            self.assertEqual(events.category, 'info')

    @mock.patch('pytrustnfe.nfse.ginfes.recepcionar_lote_rps')
    def test_nfse_connection_error_recepcionar_lote_rps(self, recepcionar_lote_rps):

        for invoice in self.invoices:

            # Cria parcelas
            invoice.generate_parcel_entry(self.financial_operation,
                                          self.title_type)

            # Confirmando a fatura deve gerar um documento eletrônico
            invoice.action_br_account_invoice_open()

            recepcionar_lote_rps.side_effect = requests.exceptions.ConnectionError(
                mock.Mock())

            invoice_electronic = self.env['invoice.electronic'].search(
                [('invoice_id', '=', invoice.id)])

            invoice_electronic.action_send_electronic_invoice()

            self.assertEqual(invoice_electronic.state, 'draft')
            self.assertEqual(invoice_electronic.codigo_retorno, 'TIMEOUT')
            self.assertTrue(invoice_electronic.mensagem_retorno)

            events = invoice_electronic.electronic_event_ids

            self.assertEqual(len(events), 1)
            self.assertEqual(events.code, 'TIMEOUT')
            self.assertEqual(events.name, invoice_electronic.mensagem_retorno)
            self.assertEqual(events.category, 'info')

    @mock.patch('pytrustnfe.nfse.ginfes.consultar_situacao_lote')
    @mock.patch('pytrustnfe.nfse.ginfes.recepcionar_lote_rps')
    def test_nfse_timeout_error_consultar_situacao_lote(self, recepcionar_lote_rps, consultar_situacao_lote):

        for invoice in self.invoices:

            # Cria parcelas
            invoice.generate_parcel_entry(self.financial_operation,
                                          self.title_type)

            # Confirmando a fatura deve gerar um documento eletrônico
            invoice.action_br_account_invoice_open()

            # Lote recebido com sucesso
            with open(os.path.join(self.caminho, 'xml', 'enviar_lote_rps_resposta.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            resp = sanitize_response(xml_recebido)

            recepcionar_lote_rps.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            elec_inv = self.env['invoice.electronic'].search(
                [('invoice_id', '=', invoice.id)])

            elec_inv.action_send_electronic_invoice()

            consultar_situacao_lote.side_effect = requests.exceptions.ConnectionError(
                mock.Mock())

            elec_inv.action_get_electronic_invoice_status()

            self.assertEqual(elec_inv.state, 'open')
            self.assertEqual(elec_inv.codigo_retorno, 'TIMEOUT')
            self.assertTrue(elec_inv.mensagem_retorno)

            events = elec_inv.electronic_event_ids

            self.assertEqual(len(events), 1)
            self.assertEqual(events.code, 'TIMEOUT')
            self.assertEqual(events.name, elec_inv.mensagem_retorno)
            self.assertEqual(events.category, 'info')

    @mock.patch('pytrustnfe.nfse.ginfes.consultar_lote_rps')
    @mock.patch('pytrustnfe.nfse.ginfes.consultar_situacao_lote')
    @mock.patch('pytrustnfe.nfse.ginfes.recepcionar_lote_rps')
    def test_nfse_timeout_error_consultar_lote_rps(self, recepcionar_lote_rps, consultar_situacao_lote, consultar_lote_rps):

        for invoice in self.invoices:

            # Cria parcelas
            invoice.generate_parcel_entry(self.financial_operation,
                                          self.title_type)

            # Confirmando a fatura deve gerar um documento eletrônico
            invoice.action_br_account_invoice_open()

            # Lote recebido com sucesso
            with open(os.path.join(self.caminho, 'xml', 'enviar_lote_rps_resposta.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            resp = sanitize_response(xml_recebido)

            recepcionar_lote_rps.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            elec_inv = self.env['invoice.electronic'].search(
                [('invoice_id', '=', invoice.id)])

            elec_inv.action_send_electronic_invoice()

            # Consulta do resultado do lote
            with open(os.path.join(self.caminho, 'xml', 'consultar_situacao_rps_resposta_3.xml'), encoding='utf-8') as xml:
                xml_recebido = xml.read().replace('\n', '')

            # testa status de retorno 3
            resp = sanitize_response(xml_recebido)

            consultar_situacao_lote.return_value = {
                'object': resp[1],
                'sent_xml': '<xml />',
                'received_xml': xml_recebido,
            }

            # Realimos o mock do metodo 'consultar_situacao_lote'
            consultar_lote_rps.side_effect = requests.exceptions.ConnectionError(
                mock.Mock())

            elec_inv.action_get_electronic_invoice_status()

            self.assertEqual(elec_inv.state, 'open')
            self.assertEqual(elec_inv.codigo_retorno, 'TIMEOUT')
            self.assertTrue(elec_inv.mensagem_retorno)

            events = elec_inv.electronic_event_ids

            self.assertEqual(len(events), 1)
            self.assertEqual(events.code, 'TIMEOUT')
            self.assertEqual(events.name, elec_inv.mensagem_retorno)
            self.assertEqual(events.category, 'info')
