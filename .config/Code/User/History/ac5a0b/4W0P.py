from warnings import catch_warnings

import pytest

from brazilcep import get_address_from_cep, WebService
from brazilcep.client import _format_cep


def test_search_error():
    with pytest.raises(KeyError):
        get_address_from_cep("37.503-130", webservice=5)

    with pytest.raises(KeyError):
        get_address_from_cep("37.503-130", webservice="VIACEP")


def test_search_correios(requests_mock):

    """Set mock get return"""
    req_mock_text = """{
        \n  "cep": "37503-130",
        \n  "logradouro": "Rua Geraldino Campista",
        \n  "complemento": "até 214/215",
        \n  "bairro": "Santo Antônio",
        \n  "localidade": "Itajubá",
        \n  "uf": "MG",
        \n  "ibge": "3132404",
        \n  "gia": "",
        \n  "ddd": "35",
        \n  "siafi": "4647"
    \n}"""

    requests_mock.get("https://ws.apicep.com/cep/37503130.json", text=req_mock_text)

    with catch_warnings(record=True) as warn:
        get_address_from_cep("37503130", webservice=WebService.CORREIOS)
        assert len(warn) == 1
        assert issubclass(warn[0].category, DeprecationWarning)

def test_format_cep_success():
    assert _format_cep("37.503-003") == "37503003"
    assert _format_cep("   37.503-003") == "37503003"
    assert _format_cep("37 503-003") == "37503003"
    assert _format_cep("37.503&003saasd") == "37503003"
    assert _format_cep("\n \r 37.503-003") == "37503003"
    assert _format_cep("\n \r 37.503-003") == "37503003"

    # ponto e virgula
    assert _format_cep("37.503-003;") == "37503003"

    # Unicode Greek Question Mark
    assert _format_cep("37.503-003;") == "37503003"


def test_format_cep_fail():

    with pytest.raises(ValueError):
        _format_cep(37503003)

    with pytest.raises(ValueError):
        _format_cep("")

    with pytest.raises(ValueError):
        _format_cep(None)

    with pytest.raises(ValueError):
        _format_cep(False)

    with pytest.raises(ValueError):
        _format_cep(True)
