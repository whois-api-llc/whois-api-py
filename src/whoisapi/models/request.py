from .base import BaseModel
from ..exceptions.error import ParameterError, EmptyApiKeyError
import re


class RequestParameters(BaseModel):
    """
    Request parameter model object. Available fields:
    - api_key
    - domain_name
    - output_format
    - prefer_fresh
    - da
    - ip
    - ip_whois
    - check_proxy_data
    - thin_whois
    - ignore_raw_texts

    Usage: instance.output_format = 'json'
    """

    _re_api_key = re.compile(r'^at_[a-z0-9]{29}$', re.IGNORECASE)
    _re_output_format = re.compile(r'^(json)|(xml)$', re.IGNORECASE)

    def __init__(self, **kwargs):
        """

        :param values: **kwargs
        Supported variables:
        - api_key - required
        - domain_name
        - output_format
        - prefer_fresh
        - da
        - ip
        - ip_whois
        - check_proxy_data
        - thin_whois
        - ignore_raw_texts
        """
        self._api_key = ''
        self._domain_name = ''
        self._output_format = 'JSON'
        self._prefer_fresh = 0
        self._da = 0
        self._ip = 0
        self._ip_whois = 0
        self._check_proxy_data = 0
        self._thin_whois = 0
        self._ignore_raw_texts = 0

        super().__init__()

        if 'api_key' in kwargs:
            self.api_key = kwargs['api_key']
        if 'domain_name' in kwargs:
            self.domain_name = kwargs['domain_name']
        if 'output_format' in kwargs:
            self.output_format = kwargs['output_format']
        if 'prefer_fresh' in kwargs:
            self.prefer_fresh = kwargs['prefer_fresh']
        if 'da' in kwargs:
            self.da = kwargs['da']
        if 'ip' in kwargs:
            self.ip = kwargs['ip']
        if 'ip_whois' in kwargs:
            self.ip_whois = kwargs['ip_whois']
        if 'check_proxy_data' in kwargs:
            self.check_proxy_data = kwargs['check_proxy_data']
        if 'thin_whois' in kwargs:
            self.thin_whois = kwargs['thin_whois']
        if 'ignore_raw_texts' in kwargs:
            self.ignore_raw_texts = kwargs['ignore_raw_texts']

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        if RequestParameters._re_api_key.search(
                str(value)
        ) is not None:
            self._api_key = str(value)
        else:
            raise ParameterError("Invalid API key format.")

    @property
    def domain_name(self):
        return self._domain_name

    @domain_name.setter
    def domain_name(self, value):
        if value is not None and len(str(value)) > 4:
            self._domain_name = str(value)
        else:
            raise ParameterError("Invalid domain name.")

    @property
    def output_format(self):
        return self._output_format

    @output_format.setter
    def output_format(self, value):
        if RequestParameters._re_output_format.search(str(value)):
            self._output_format = str(value)
        else:
            raise ParameterError(
                "Output format should either JSON or XML.")

    @property
    def prefer_fresh(self):
        return self._prefer_fresh

    @prefer_fresh.setter
    def prefer_fresh(self, value):
        if int(value) in [0, 1]:
            self._prefer_fresh = int(value)
        else:
            raise ParameterError("'prefer_fresh' should be 0 or 1.")

    @property
    def da(self):
        return self._da

    @da.setter
    def da(self, value):
        if int(value) in [0, 1, 2]:
            self._da = int(value)
        else:
            raise ParameterError("'da' should be 0, 1 or 2.")

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        if int(value) in [0, 1]:
            self._ip = int(value)
        else:
            raise ParameterError("'ip' should be 0 or 1.")

    @property
    def ip_whois(self):
        return self._ip_whois

    @ip_whois.setter
    def ip_whois(self, value):
        if int(value) in [0, 1]:
            self._ip_whois = int(value)
        else:
            raise ParameterError("'ip_whois' should be 0 or 1.")

    @property
    def check_proxy_data(self):
        return self._check_proxy_data

    @check_proxy_data.setter
    def check_proxy_data(self, value):
        if int(value) in [0, 1]:
            self._check_proxy_data = int(value)
        else:
            raise ParameterError("'check_proxy_data' should be 0 or 1.")

    @property
    def thin_whois(self):
        return self._thin_whois

    @thin_whois.setter
    def thin_whois(self, value):
        if int(value) in [0, 1]:
            self._thin_whois = int(value)
        else:
            raise ParameterError("'thin_whois' should be 0 or 1.")

    @property
    def ignore_raw_texts(self):
        return self._ignore_raw_texts

    @ignore_raw_texts.setter
    def ignore_raw_texts(self, value):
        if int(value) in [0, 1]:
            self._ignore_raw_texts = int(value)
        else:
            raise ParameterError("'ignore_raw_texts' should be 0 or 1.")

    def get_request_parameters(self):
        if self.api_key == '':
            raise EmptyApiKeyError("API key isn't defined")
        return {
            'apiKey': self.api_key,
            'domainName': self.domain_name,
            'outputFormat': self.output_format,
            'da': self.da,
            'ip': self.ip,
            'ipWhois': self.ip_whois,
            'thinWhois': self.thin_whois,
            'preferFresh': self.prefer_fresh,
            'checkProxyData': self.check_proxy_data,
            'ignoreRawTexts': self.ignore_raw_texts
        }
