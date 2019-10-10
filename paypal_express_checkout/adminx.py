"""Admins for the models of the ``paypal_express_checkout`` app."""
import django.contrib.auth
import xadmin.sites
from django.utils.translation import ugettext_lazy as _

from . import models
from .utils import get_currency_model

try:
    user_model = django.contrib.auth.get_user_model()
except AttributeError:
    user_model = django.contrib.auth.models.User

username_field = getattr(user_model, 'USERNAME_FIELD', 'username')


class ItemAdmin(object):
    """Custom admin for the ``Item`` model."""
    list_display = ['name', 'description_short', 'user', 'value']
    search_fields = ['name', 'description']

    def description_short(self, obj):
        return '{0}...'.format(obj.description[:50])


class PaymentTransactionAdmin(object):
    """Custom admin for the ``PaymentTransaction`` model."""
    list_display = [
        'date', 'user', 'user_email', 'transaction_id',
        'list_display_value', 'status',
    ]
    exclude = ["completed"]
    search_fields = [
        'transaction_id', 'status', 'user__email', 'user__' + username_field]
    date_hierarchy = 'creation_date'
    list_filter = ['status', 'creation_date']
    raw_id_fields = ['user', ]

    def list_display_value(self, instance):
        return "{0.currency.sign} {0.value}".format(instance)
    list_display_value.short_description = _("Value")
    list_display_value.is_column = True
    list_display_value.admin_order_field = "value"

    def user_email(self, obj):
        return obj.user.email


class PaymentTransactionErrorAdmin(object):
    """Custom admin for the ``PaymentTransactionError`` model."""
    list_display = [
        # FIXME 'transaction_id'
        'date', 'user', 'user_email', 'response_short',
    ]

    def user_email(self, obj):
        return obj.user.email

    def response_short(self, obj):
        return '{0}...'.format(obj.response[:50])

    def transaction_id(self, obj):
        return obj.transaction_id


class PurchasedItemAdmin(object):
    """Custom admin for the ``PurchasedItem`` model."""
    list_display = [
        'date', 'list_display_user', 'transaction', 'item',
        'price', 'quantity', 'subtotal', 'total', 'status',
    ]
    list_filter = [
        'identifier', 'transaction__status', 'item', ]
    search_fields = [
        'transaction__transaction_id', 'user__email', ]
    raw_id_fields = ['user', 'transaction', ]

    def list_display_user(self, instance):
        user = instance.user
        if hasattr(user, 'email'):
            return user.email
        else:
            return str(user)

    list_display_user.short_description = _("User")
    list_display_user.is_column = True
    list_display_user.admin_order_field = "user"

    def date(self, obj):
        return obj.transaction.date

    def status(self, obj):
        return obj.transaction.status

    def subtotal(self, obj):
        price = 0
        if obj.item is not None:
            price = obj.item.value
        if obj.price:
            price = obj.price
        return price * obj.quantity

    def total(self, obj):
        return obj.transaction.value

    def user_email(self, obj):
        return obj.user.email


class CurrencyAdmin(object):
    """Currency Admin"""


try:
    xadmin.sites.site.register(get_currency_model(), CurrencyAdmin)
except xadmin.sites.AlreadyRegistered:
    pass # just ignore

xadmin.sites.site.register(models.Item, ItemAdmin)
xadmin.sites.site.register(models.PaymentTransaction, PaymentTransactionAdmin)
xadmin.sites.site.register(models.PurchasedItem, PurchasedItemAdmin)
xadmin.sites.site.register(models.PaymentTransactionError, PaymentTransactionErrorAdmin)
