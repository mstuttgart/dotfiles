# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os

from lxml import etree
from requests import Session
from zeep import Client
from zeep.transports import Transport
from requests.packages.urllib3 import disable_warnings

from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.nfse.assinatura import Assinatura

def _render(certificado, method, **kwargs):

    if kwargs['emissor'] == 'fortaleza':

        # o servico de cancelamento de fortaleza tem outro nome
        if method == "CancelarNfseV3":
            method = "CancelarNfse"

    path = os.path.join(os.path.dirname(__file__), "templates")
    xml_send = render_xml(path, "%s.xml" % method, True, **kwargs)

    if type(xml_send) != str:
        xml_send = etree.tostring(xml_send)

    reference = ""

    if method in ("RecepcionarLoteRpsV3", "RecepcionarLoteRpsSincronoV3"):
        reference = "rps%s" % kwargs["nfse"]["lista_rps"][0]["numero"]

    elif method == ("CancelarNfseV3", "CancelarNfse"):
        reference = "C%s" % kwargs["cancelamento"]["numero_nfse"]

    cert, key = extract_cert_and_key_from_pfx(certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)
    signer = Assinatura(cert, key, certificado.password)
    xml_send = signer.assina_xml(xml_send, "")

    return xml_send

def _send(certificado, method, **kwargs):
    base_url = ""

    if kwargs['emissor'] == 'fortaleza':

        # fortaleza utiliza webservice diferente
        if kwargs["ambiente"] == "producao":
            base_url = "https://iss.fortaleza.ce.gov.br/grpfor-iss/ServiceGinfesImplService?wsdl"
        else:
            base_url = "http://isshomo.sefin.fortaleza.ce.gov.br/grpfor-iss/ServiceGinfesImplService"

        # o servico de cancelamento de fortaleza tem outro nome
        if method == "CancelarNfseV3":
            method = "CancelarNfse"

    else:

        if kwargs["ambiente"] == "producao":
            base_url = "https://producao.ginfes.com.br/ServiceGinfesImpl?wsdl"
        else:
            base_url = "https://homologacao.ginfes.com.br/ServiceGinfesImpl?wsdl"

    cert, key = extract_cert_and_key_from_pfx(certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)

    # Para o cancelamento, deve usar o template da versao 2 ao inves da 3 (so o ginfes sabe o motivo)
    if method == "CancelarNfseV3":
        header = '<ns2:cabecalho xmlns:ns2="http://www.ginfes.com.br/cabecalho_v03.xsd" xmlns:tipos="http://www.ginfes.com.br/tipos_v03.xsd" versao="2"><versaoDados>2</versaoDados></ns2:cabecalho>'  # noqa
    if method == "CancelarNfse":
        # 
        header = None
    else:
        header = '<ns2:cabecalho xmlns:ns2="http://www.ginfes.com.br/cabecalho_v03.xsd" xmlns:tipos="http://www.ginfes.com.br/tipos_v03.xsd" versao="3"><versaoDados>3</versaoDados></ns2:cabecalho>'  # noqa

    disable_warnings()
    session = Session()
    session.cert = (cert, key)
    session.verify = False
    transport = Transport(session=session, operation_timeout=240)

    # import ipdb; ipdb.set_trace()  # noqa


    client = Client(base_url, transport=transport)

    xml_send = kwargs["xml"]
    response = client.service[method](header, xml_send)

    response, obj = sanitize_response(response)
    return {"sent_xml": xml_send, "received_xml": response, "object": obj}


def xml_recepcionar_lote_rps(certificado, **kwargs):
    return _render(certificado, "RecepcionarLoteRpsV3", **kwargs)


def recepcionar_lote_rps(certificado, **kwargs):

    if "xml" not in kwargs:
        kwargs["xml"] = xml_recepcionar_lote_rps(certificado, **kwargs)
    return _send(certificado, "RecepcionarLoteRpsV3", **kwargs)


def xml_recepcionar_lote_rps_sync(certificado, **kwargs):
    return _render(certificado, "RecepcionarLoteRpsSincronoV3", **kwargs)


def recepcionar_lote_rps_sync(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_recepcionar_lote_rps(certificado, **kwargs)
    return _send(certificado, "RecepcionarLoteRpsSincronoV3", **kwargs)


def xml_consultar_situacao_lote(certificado, **kwargs):
    return _render(certificado, "ConsultarSituacaoLoteRpsV3", **kwargs)


def consultar_situacao_lote(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_consultar_situacao_lote(certificado, **kwargs)
    return _send(certificado, "ConsultarSituacaoLoteRpsV3", **kwargs)


def xml_consultar_nfse_por_rps(certificado, **kwargs):
    return _render(certificado, "ConsultarNfsePorRpsV3", **kwargs)

def consultar_nfse_por_rps(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_consultar_nfse_por_rps(certificado, **kwargs)

    return _send(certificado, "ConsultarNfsePorRpsV3", **kwargs)

def xml_consultar_lote_rps(certificado, **kwargs):
    return _render(certificado, "ConsultarLoteRpsV3", **kwargs)


def consultar_lote_rps(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_consultar_lote_rps(certificado, **kwargs)
    return _send(certificado, "ConsultarLoteRpsV3", **kwargs)

def xml_consultar_nfse(certificado, **kwargs):
    return _render(certificado, "ConsultarNfseV3", **kwargs)

def consultar_nfse(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_consultar_nfse(certificado, **kwargs)

    return _send(certificado, "ConsultarNfseV3", **kwargs)

def xml_cancelar_nfse(certificado, **kwargs):
    return _render(certificado, "CancelarNfse", **kwargs)


def cancelar_nfse(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_cancelar_nfse(certificado, **kwargs)
    return _send(certificado, "CancelarNfse", **kwargs)
