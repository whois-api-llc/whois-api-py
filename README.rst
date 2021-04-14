.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :alt: whois-api-py license
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/pypi/v/whois-api.svg
    :alt: whois-api-py release
    :target: https://pypi.org/project/whois-api

.. image:: https://github.com/whois-api-llc/whois-api-py/workflows/Build/badge.svg
    :alt: whois-api-py build
    :target: https://github.com/whois-api-llc/whois-api-py/actions

========
Overview
========

The client library for
`Whois API <https://whois.whoisxmlapi.com/>`_
in Python language.

The minimum Python version is 3.6.

Installation
============
::

    pip install whois-api

Examples
========

Full API documentation available `here <https://whois.whoisxmlapi.com/api/documentation/making-requests>`_

Create a new client
-------------------

::

    from whoisapi import *

    client = Client(api_key='Your API key')

Make basic requests
-------------------

::

    # Get parsed whois record as a model instance.
    whois = client.data('whoisxmlapi.com')
    # Get particular field of the whois record
    print(whois.created_date_raw)

    # Get raw API response
    resp_str = client.raw_data('whoisxmlapi.com')

Additional options
-------------------
You can specify a custom parameters for particular request


::

    params = RequestParameters(ignore_raw_texts=1, da=2)

    whois = client.data('whoisxmlapi.com', params)
    print(whois.domain_availability_raw)

    # Also you can modify default values of parameters:
    client.parameters.output_format = 'xml'
    print(client.raw_data('whoisxmlapi.com'))
