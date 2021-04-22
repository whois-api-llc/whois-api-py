
class WhoisApiError(Exception):
    def __init__(self, message):
        self.message = message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message

    def __str__(self):
        return str(self.__dict__)


class ParameterError(WhoisApiError):
    pass


class EmptyApiKeyError(WhoisApiError):
    pass


class ResponseError(WhoisApiError):
    def __init__(self, message, parsed_message):
        self.message = message
        self.parsed_message = parsed_message

    @property
    def parsed_message(self):
        return self._parsed_message

    @parsed_message.setter
    def parsed_message(self, pm):
        self._parsed_message = pm


class UnparsableApiResponseError(WhoisApiError):
    def __init__(self, message, origin_error):
        self.message = message
        self.original_error = origin_error

    @property
    def original_error(self):
        return self._original_error

    @original_error.setter
    def original_error(self, oe):
        self._original_error = oe


class ApiAuthError(WhoisApiError):
    pass


class HttpApiError(WhoisApiError):
    pass
