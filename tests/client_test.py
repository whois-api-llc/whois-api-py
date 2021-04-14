import os
import unittest
from whoisapi import Client
from whoisapi import ResponseError
from whoisapi import ApiAuthError
from whoisapi import RequestParameters


class TestClient(unittest.TestCase):
    """
    Final integration test without mocks.

    Active API_KEY is required.
    """
    def test_get_correct_data(self):
        client = Client(api_key=os.getenv("API_KEY"))

        date = '2009-03-19 21:47:17'
        whois = client.data('whoisxmlapi.com')
        assert whois.created_date.strftime("%Y-%m-%d %H:%M:%S") == date

    def test_get_raw(self):
        client = Client(api_key=os.getenv('API_KEY'))
        response = client.raw_data('whoisxmlapi.com')
        assert 'WhoisRecord' in response

    def test_get_incorrect(self):
        client = Client(api_key=os.getenv('API_KEY'))
        whois = client.data('incorrect.incorrect')
        assert whois.data_error == 'INVALID_TLD'

    def test_get_invalid_domain(self):
        client = Client(api_key=os.getenv('API_KEY'))
        self.assertRaises(ResponseError, client.data, 'not-a-domain')

    def test_get_raw_xml(self):
        client = Client(api_key=os.getenv('API_KEY'))
        client.parameters.output_format = 'XML'
        response = client.raw_data('whoisxmlapi.com')
        assert response.startswith('<?xml version="1.0"')

    def test_invalid_api_key(self):
        client = Client(api_key='at_00000000000000000000000000000')
        self.assertRaises(ApiAuthError, client.data, 'whoisxmlapi.com')

    def test_custom_request_parameters(self):
        api_key = os.getenv('API_KEY')
        client = Client(api_key=api_key)
        whois = client.data('whoisxmlapi.com')
        assert whois.domain_availability is None
        assert len(whois.raw_text) > 20
        params = RequestParameters(ignore_raw_texts=1, da=2)
        whois2 = client.data('whoisxmlapi.com', params)
        assert whois2.domain_availability is False
        assert whois2.raw_text == ''


if __name__ == '__main__':
    unittest.main()
