"""Signals for the ``paypal_express_checkout`` app."""
from django.dispatch import Signal


# A signal that arrives, when an IPN is received with status 'Completed'
payment_completed = Signal(providing_args=['transaction', 'ipn_data'])
payment_status_updated = Signal(providing_args=['transaction', 'ipn_data'])
