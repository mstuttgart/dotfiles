"""
brazilcep.viacep
~~~~~~~~~~~~~~~~

This module implements the BrazilCEP BrasilAPI adapter.

:copyright: (c) 2023 by Michell Stuttgart.
:license: MIT, see LICENSE for more details.
"""

import json

import requests

from . import exceptions

URL = "brasilapi.com.br/api/cep/v1/{}"


def fetch_address(cep, timeout):
    """Fetch APICEP webservice for CEP address. APICEP provide
    a REST API to query CEP requests.

    Args:
        cep (str):CEP to be searched.

    Returns:
        address (dict): respective address data from CEP.
    """

    response = requests.get(URL.format(cep), timeout=timeout)

    if response.status_code == 200:
        # Transforma o objeto requests em um dict
        address = json.loads(response.text)

        if address.get("erro"):
            raise exceptions.CEPNotFound()

        return {
            "district": address.get("neighborhood") or "",
            "cep": address.get("cep") or "",
            "city": address.get("city") or "",
            "street": address.get("logradouro") or "",
            "uf": address.get("state") or "",
            "complement": address.get("complemento") or "",
        }

    if response.status_code == 400:
        raise exceptions.InvalidCEP()

    raise exceptions.BrazilCEPException(
        f"Other error. Status code: {response.status_code}"
    )
