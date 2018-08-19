"""Utilities for the paypal_express_checkout app."""
import urllib.parse

from django.apps import apps
from django.utils import six

from . import models


def urlencode(data):
    """Analyze date and convert values to utf-8"""
    for key, value in six.iteritems(data):
        data[key] = str(value).encode('utf-8')
    return urllib.parse.urlencode(data)


def get_currency_model():
    """Returns the Currency model of the configuration"""
    if isinstance(models.Currency, str):
        return apps.get_model(*models.Currency.split("."))
    return models.Currency
