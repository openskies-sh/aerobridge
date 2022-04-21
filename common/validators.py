from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from moneyed import CURRENCIES



import re


def validate_currency_code(code):
    """
    Check that a given code is a valid currency code.
    """

    if code not in CURRENCIES:
        raise ValidationError(_('Not a valid currency code'))

