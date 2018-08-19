from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PaypalExpressCheckoutConfig(AppConfig):
    verbose_name = _("PAYPAL EXPRESS CHECKOUT")
    name = 'paypal_express_checkout'

    def ready(self):
        """"""
