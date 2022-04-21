from __future__ import unicode_literals

from moneyed import CURRENCIES
from django.conf import settings

from os import environ as env
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())



def currency_code_default():
    """
    Returns the default currency code (or INR if not specified)
    """
    
    code = env.get('AEROBRIDGE_DEFAULT_CURRENCY', None)
    
    if code not in CURRENCIES:
        code = 'INR'  # pragma: no cover

    return code


def currency_code_mappings():
    """
    Returns the current currency choices
    """
    return [(a, CURRENCIES[a].name) for a in settings.CURRENCIES]


def currency_codes():
    """
    Returns the current currency codes
    """
    return [a for a in settings.CURRENCIES]
