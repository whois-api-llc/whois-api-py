import datetime
import copy
import re
import logging
from .base import BaseModel


_logger = logging.getLogger('whois-api-client-models')

re_timezone_offset = re.compile(r'([-+])(\d\d)(:)?(\d\d)$')
re_coordinated_utc = re.compile(r'(T\d\d:\d\d:\d\dZ)$')
re_milliseconds_and_timezone_name = re.compile(
    r'(\.\d\d\d)?\s+([a-z]{3,4})$', re.IGNORECASE)


def _string_value(values: dict, key: str) -> str:
    if key in values:
        return str(values[key])
    return ''


def _int_value(values: dict, key: str) -> int:
    if key in values:
        try:
            return int(values[key])
        except (ValueError, Exception) as error:
            _logger.error(
            "Couldn't parse the int ({}: {}). Error occurred: {}".format(
                key,
                values[key],
                error.__str__()
            )
        )
    return 0


def _list_value(values: dict, key: str) -> list:
    if key in values and type(values[key]) is list:
        return copy.deepcopy(values[key])
    return []


def _datetime_value(values: dict, key: str) -> datetime.datetime or None:
    if key in values:
        if values[key] is None:
            return None
        dt = str(values[key])
        m = re_timezone_offset.search(dt)
        m2 = re_milliseconds_and_timezone_name.search(dt)
        m3 = re_coordinated_utc.search(dt)
        try:
            if m is not None:
                return datetime.datetime.strptime(
                    re_timezone_offset.sub(r'\1\2\4', dt),
                    "%Y-%m-%dT%H:%M:%S%z")
            if m2 is not None:
                return datetime.datetime.strptime(
                    re_milliseconds_and_timezone_name.sub(r' \2', dt),
                    "%Y-%m-%d %H:%M:%S %Z")
            if m3 is not None:
                return datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ')
        except (ValueError, Exception) as error:
            _logger.error(
                "Couldn't parse the date ({}). Error occurred: {}".format(
                    dt,
                    error.__str__()
                )
            )

        return None


class NameServers(BaseModel):
    raw_text: str
    host_names: list
    ips: list

    def __init__(self, values):
        super().__init__()
        self.raw_text = ''
        self.host_names = []
        self.ips = []

        if values is not None:
            self.raw_text = _string_value(values, 'rawText')
            self.host_names = _list_value(values, 'hostNames')
            self.ips = _list_value(values, 'ips')


class Audit(BaseModel):
    created_date: datetime.datetime or None
    created_date_raw: str
    updated_date: datetime.datetime or None
    updated_date_raw: str

    def __init__(self, values):
        super().__init__()
        self.updated_date = None
        self.created_date = None
        self.updated_date_raw = ''
        self.created_date_raw = ''

        if values is not None:
            self.updated_date = _datetime_value(values, 'updatedDate')
            self.updated_date_raw = _string_value(values, 'updatedDate')
            self.created_date = _datetime_value(values, 'createdDate')
            self.created_date_raw = _string_value(values, 'createdDate')


class Record(BaseModel):
    def __init__(self):
        super().__init__()


class Contact(BaseModel):
    name: str
    organization: str
    street1: str
    street2: str
    street3: str
    street4: str
    city: str
    state: str
    postal_code: int
    country: str
    country_code: str
    email: str
    telephone: str
    telephone_ext: str
    fax: str
    fax_ext: str
    raw_text: str

    def __init__(self, values):
        super().__init__()
        self.name = ''
        self.organization = ''
        self.street1 = ''
        self.street2 = ''
        self.street3 = ''
        self.street4 = ''
        self.city = ''
        self.state = ''
        self.postal_code = 0
        self.country = ''
        self.country_code = ''
        self.email = ''
        self.telephone = ''
        self.telephone_ext = ''
        self.fax = ''
        self.fax_ext = ''

        if values is not None:
            self.name = _string_value(values, 'name')
            self.organization = _string_value(values, 'organization')
            self.street1 = _string_value(values, 'street1')
            self.street2 = _string_value(values, 'street2')
            self.street3 = _string_value(values, 'street3')
            self.street4 = _string_value(values, 'street4')
            self.city = _string_value(values, 'city')
            self.state = _string_value(values, 'state')
            self.postal_code = _int_value(values, 'postalCode')
            self.country = _string_value(values, 'country')
            self.country_code = _string_value(values, 'countryCode')
            self.email = _string_value(values, 'email')
            self.telephone = _string_value(values, 'telephone')
            self.telephone_ext = _string_value(values, 'telephoneExt')
            self.fax = _string_value(values, 'fax')
            self.fax_ext = _string_value(values, 'faxExt')


class Registrant(Contact):
    unparsable: str

    def __init__(self, values):
        super().__init__(values)
        self.unparsable = ''

        if values is not None:
            self.unparsable = _string_value(values, 'unparsable')


class BaseWhoisRecord(Record):
    created_date: datetime.datetime or None
    created_date_raw: str
    updated_date: datetime.datetime or None
    updated_date_raw: str
    expires_date: datetime.datetime or None
    expires_date_raw: str
    data_error: str
    contact_email: str
    custom1_field_name: str
    custom1_field_value: str
    custom2_field_name: str
    custom2_field_value: str
    custom3_field_name: str
    custom3_field_value: str
    domain_availability: bool or None
    domain_availability_raw: str
    domain_name: str
    domain_name_ext: str
    estimated_domain_age: int
    estimated_domain_age_raw: str
    footer: str
    header: str
    audit: Audit or None
    name_servers: NameServers or None
    parse_code: int
    raw_text: str
    stripped_text: str
    registrant: Registrant or None
    administrative_contact: Contact or None
    billing_contact: Contact or None
    technical_contact: Contact or None
    zone_contact: Contact or None
    registrar_name: str
    registrar_ianaid: str
    created_date_normalized: datetime.datetime or None
    updated_date_normalized: datetime.datetime or None
    expires_date_normalized: datetime.datetime or None
    whois_server: str

    def __init__(self, values):
        super().__init__()
        self.created_date = None
        self.created_date_raw = ""
        self.updated_date = None
        self.updated_date_raw = ""
        self.expires_date = None
        self.expires_date_raw = ''
        self.data_error = ''
        self.contact_email = ''
        self.custom1_field_name = ''
        self.custom1_field_value = ''
        self.custom2_field_name = ''
        self.custom2_field_value = ''
        self.custom3_field_name = ''
        self.custom3_field_value = ''
        self.domain_availability = None
        self.domain_availability_raw = ''
        self.domain_name = ''
        self.domain_name_ext = ''
        self.estimated_domain_age = 0
        self.estimated_domain_age_raw = ''
        self.footer = ''
        self.header = ''
        self.audit = None
        self.name_servers = None
        self.parse_code = 0
        self.raw_text = ''
        self.stripped_text = ''
        self.registrant = None
        self.administrative_contact = None
        self.billing_contact = None
        self.technical_contact = None
        self.zone_contact = None
        self.registrar_name = ''
        self.registrar_ianaid = ''
        self.whois_server = ''
        self.created_date_normalized = None
        self.updated_date_normalized = None
        self.expires_date_normalized = None

        if values is not None:
            self.created_date = _datetime_value(values, 'createdDate')
            self.created_date_raw = _string_value(values, 'createdDate')
            self.updated_date = _datetime_value(values, 'updatedDate')
            self.updated_date_raw = _string_value(values, 'updatedDate')
            self.expires_date = _datetime_value(values, 'expiresDate')
            self.expires_date_raw = _string_value(values, 'expiresDate')
            self.data_error = _string_value(values, 'dataError')
            self.contact_email = _string_value(values, 'contactEmail')
            self.custom1_field_name = _string_value(values, 'custom1FieldName')
            self.custom1_field_value = _string_value(values, 'custom1FieldValue')
            self.custom2_field_name = _string_value(values, 'custom2FieldName')
            self.custom2_field_value = _string_value(values, 'custom2FieldValue')
            self.custom3_field_name = _string_value(values, 'custom3FieldName')
            self.custom3_field_value = _string_value(values, 'custom3FieldValue')
            self.domain_availability = BaseWhoisRecord._parse_domain_availability(
                _string_value(values, 'domainAvailability'))
            self.domain_availability_raw = _string_value(values, 'domainAvailability')
            self.domain_name = _string_value(values, 'domainName')
            self.domain_name_ext = _string_value(values, 'domainNameExt')
            self.estimated_domain_age = _int_value(values, 'estimatedDomainAge')
            self.estimated_domain_age_raw = _string_value(values, 'estimatedDomainAge')
            self.footer = _string_value(values, 'footer')
            self.header = _string_value(values, 'header')
            if 'audit' in values:
                self.audit = Audit(values['audit'])
            if 'nameServers' in values:
                self.name_servers = NameServers(values['nameServers'])
            self.parse_code = _int_value(values, 'parseCode')
            self.raw_text = _string_value(values, 'rawText')
            self.stripped_text = _string_value(values, 'strippedText')
            if 'registrant' in values:
                self.registrant = Registrant(values['registrant'])
            if 'administrativeContact' in values:
                self.administrative_contact = Contact(values['administrativeContact'])
            if 'billingContact' in values:
                self.billing_contact = Contact(values['billingContact'])
            if 'technicalContact' in values:
                self.technical_contact = Contact(values['technicalContact'])
            if 'zoneContact' in values:
                self.zone_contact = Contact(values['zoneContact'])
            self.registrar_name = _string_value(values, 'registrarName')
            self.registrar_ianaid = _string_value(values, 'registrarIANANID')
            self.whois_server = _string_value(values, 'whoisServer')
            self.created_date_normalized = _datetime_value(values, 'createdDateNormalized')
            self.updated_date_normalized = _datetime_value(values, 'updatedDateNormalized')
            self.expires_date_normalized = _datetime_value(values, 'expiresDateNormalized')

    @staticmethod
    def _parse_domain_availability(value) -> bool or None:
        if str(value).lower() == 'available':
            return True
        if str(value).lower() == 'unavailable':
            return False
        return None


class RegistryData(BaseWhoisRecord):
    referral_url: str
    status: str

    def __init__(self, values):
        super().__init__(values)

        self.referral_url = ''
        self.status = ''

        if values is not None:
            self.referral_url = _string_value(values, 'referralURL')
            self.status = _string_value(values, 'status')


class WhoisRecord(BaseWhoisRecord):
    registry_data: RegistryData or None

    def __init__(self, values):
        super().__init__(values)
        self.registry_data = None

        if values is not None:
            if 'registryData' in values:
                self.registry_data = RegistryData(values['registryData'])


class ErrorMessage(Record):
    msg: str
    error_code: str

    def __init__(self, values):
        super().__init__()

        self.msg = ''
        self.error_code = ''

        if values is not None:
            self.error_code = _string_value(values, 'errorMessage')
            self.msg = _string_value(values, 'msg')
