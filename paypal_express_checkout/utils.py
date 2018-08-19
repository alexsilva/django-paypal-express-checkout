"""Utilities for the paypal_express_checkout app."""
import urllib.parse

from django.utils import six


def urlencode(data):
    """Analyze date and convert values to utf-8"""
    for key, value in six.iteritems(data):
        data[key] = str(value).encode('utf-8')
    return urllib.parse.urlencode(data)
