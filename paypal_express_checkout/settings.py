"""Settings for the ``paypal_express_checkout`` app."""
from django.conf import settings

Currency = getattr(
    settings, "PAYPAL_EXPRESS_CHECKOUT_CURRENCY_MODEL",
    None)

SET_CHECKOUT_FORM = getattr(
    settings, 'PAYPAL_SET_CHECKOUT_FORM',
    'paypal_express_checkout.forms.SetExpressCheckoutItemForm')

LOGIN_URL = getattr(
    settings, 'PAYPAL_LOGIN_URL',
    'https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token=')

API_URL = getattr(
    settings, 'PAYPAL_API_URL',
    'https://api-3t.paypal.com/nvp')

ALLOW_ANONYMOUS_CHECKOUT = getattr(
    settings, 'PAYPAL_ALLOW_ANONYMOUS_CHECKOUT',
    False)
