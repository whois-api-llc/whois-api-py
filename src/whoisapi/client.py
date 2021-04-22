from json import loads, JSONDecodeError

from .models.request import RequestParameters
from .net.http import ApiRequester
from .models.response import WhoisRecord, ErrorMessage
from .exceptions.error import ResponseError, UnparsableApiResponseError


class Client:
    __default_url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
    __parsable_format = 'json'
    _api_requester: ApiRequester or None

    def __init__(self, **kwargs):
        """

        :param kwargs: dict Supported parameters:
        - url: (optional) API endpoint URL; str
        - timeout: (optional) API call timeout in seconds; float
        One of the following parameters (required):
        - api_key: Your API key; str
        - parameters: RequestParameters
        """
        if 'url' not in kwargs:
            kwargs['url'] = Client.__default_url
        self.api_requester = ApiRequester(**kwargs)

    @property
    def parameters(self) -> RequestParameters:
        return self._api_requester.parameters

    @parameters.setter
    def parameters(self, value: RequestParameters):
        self._api_requester.parameters = value

    @property
    def api_requester(self) -> ApiRequester or None:
        return self._api_requester

    @api_requester.setter
    def api_requester(self, value: ApiRequester):
        self._api_requester = value

    @property
    def timeout(self) -> float:
        return self._api_requester.timeout

    @timeout.setter
    def timeout(self, value: float):
        self._api_requester.timeout = value

    def data(self, domain: str,
             params: RequestParameters or None = None) -> WhoisRecord:
        """
        Get parsed whois data from the API
        :param domain: str - the domain name
        :param params: RequestParameters instance (optional)
        :return: WhoisRecord
        :raises
        - base class is whoisapi.exceptions.WhoisApiError
          - ResponseError -- the response contain ErrorMessage
          - UnparsableApiResponseError -- the response couldn't be parsed
          - ApiAuthError -- Server returns 401 HTTP code
          - HttpApiError -- HTTP code is not 2xx or 401
        - ConnectionError
        """
        if params is None:
            params = self._api_requester.parameters
        params.output_format = Client.__parsable_format
        response = self._api_requester.get_data(domain, params)
        try:
            parsed = loads(str(response))
            if 'ErrorMessage' in parsed:
                error = ErrorMessage(parsed['ErrorMessage'])
                raise ResponseError(response, error)
            if 'WhoisRecord' in parsed:
                return WhoisRecord(parsed['WhoisRecord'])
            raise UnparsableApiResponseError(
                "Could not find a correct root element.", None)
        except JSONDecodeError as error:
            raise UnparsableApiResponseError("Could not parse API response", error)

    def raw_data(self, domain: str,
                 params: RequestParameters or None = None) -> str:
        if params is None:
            params = self._api_requester.parameters
        return self._api_requester.get_data(domain, params)
