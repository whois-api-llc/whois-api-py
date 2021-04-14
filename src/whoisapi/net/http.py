from requests import request
from ..models.request import RequestParameters
from ..exceptions.error import ParameterError, \
    ApiAuthError, HttpApiError
import logging


class ApiRequester:
    __logger = logging.getLogger("whois-api-requester")
    __connect_timeout = 5
    _base_url: str
    _parameters: RequestParameters or None
    _timeout: float

    def __init__(self, **kwargs):
        """

        :param kwargs: Supported parameters:
        - url: API endpoint URL; str
        - timeout: (optional) API call timeout in seconds; float
        One of the following parameters (required):
        - api_key: Your API key; str
        - parameters: RequestParameters
        """
        self._base_url = ''
        self._parameters = None
        self.timeout = 30

        if 'url' in kwargs:
            self.base_url = kwargs.get('url')
        if 'api_key' in kwargs and 'parameters' not in kwargs:
            self.parameters = RequestParameters(
                api_key=kwargs.get('api_key')
            )
        if 'parameters' in kwargs \
                and isinstance(kwargs['parameters'], RequestParameters):
            self.parameters = kwargs['parameters']
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']

        if self.parameters is None:
            raise ParameterError("Either 'api_key' or 'parameters' required.")

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, url: str):
        if url is None or len(url) <= 8 or not url.startswith('http'):
            raise ValueError("Invalid URL specified.")
        self._base_url = url

    @property
    def parameters(self) -> RequestParameters or None:
        return self._parameters

    @parameters.setter
    def parameters(self, params: RequestParameters):
        if params is not None and isinstance(params, RequestParameters):
            self._parameters = params
        else:
            raise TypeError(
                "params should instance of RequestParameters class")

    @property
    def timeout(self) -> float:
        """API call timeout in seconds"""
        return self._timeout

    @timeout.setter
    def timeout(self, value: float):
        """API call timeout in seconds"""
        if value is not None and 1 <= value <= 60:
            self._timeout = value
        else:
            raise ValueError("Timeout value should be in [1, 60]")

    def api_key(self, key: str):
        self.parameters['api_key'] = key

    def get_data(self, domain, params=None):
        if params is not None and isinstance(params, RequestParameters):
            if params.api_key == '':
                params.api_key = self.parameters.api_key
            payload = params.get_request_parameters()
        else:
            payload = self.parameters.get_request_parameters()
        payload['domainName'] = domain or payload['domainName']

        response = request(
            "GET",
            self.base_url,
            params=payload,
            timeout=(ApiRequester.__connect_timeout, self.timeout)
        )

        if 200 <= response.status_code < 300:
            return response.text

        if response.status_code == 401:
            raise ApiAuthError(response.text)

        if response.status_code >= 300:
            raise HttpApiError(response.text)
