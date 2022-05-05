from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse
from moneyed import CURRENCIES
#import re


def validate_currency_code(code):
    """
    Check that a given code is a valid currency code.
    """
    if code not in CURRENCIES:
        raise ValidationError(_('Not a valid currency code'))

def validate_url(value):
    if not value:
        return  # Required error is done the field
    parsed_url = urlparse(value)
    if not bool(parsed_url.scheme):
        raise ValidationError('Only valid urls are allowed')


def validate_flight_controller_id(value):
    if not value.isalnum():
        raise ValidationError(u'%s flight controller ID cannot contain special characters or spaces' % value)
