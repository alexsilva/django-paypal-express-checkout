"""The models for the ``paypal_express_checkout`` app."""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import gettext as _

from .constants import STATUS_CHOICES
from .settings import Currency

if Currency is None:

    @python_2_unicode_compatible
    class Currency(models.Model):
        """Currency model"""
        sign = models.CharField(verbose_name=_("Sign"),
                                help_text=_("Sign of the currency of exchange. ex: $"),
                                max_length=32)
        code = models.CharField(verbose_name=_("Code"),
                                help_text=_("Currency code. ex: USD"),
                                max_length=32)
        description = models.CharField(verbose_name=_("Description"),
                                       max_length=255,
                                       help_text=_("Description of currency"),
                                       blank=True, null=True)

        def __str__(self):
            return "{0.description} ({0.sign})".format(self)

        class Meta:
            verbose_name = _("Currency")
            verbose_name_plural = _("Currencies")


@python_2_unicode_compatible
class Item(models.Model):
    """
    Holds the information about an item, that is on Sale.

    The information will be needed to process the PayPal payment transaction.

    :identifier: A unique identifier for the item.
    :name: Name of the item.
    :description: Description of the item.
    :value: The price of the item.
    :currency: Short currency identifier. Defaults to USD.

    """
    identifier = models.CharField(
        max_length=256,
        verbose_name=_('Identifier'),
        blank=True,
    )

    name = models.CharField(
        max_length=2048,
        verbose_name=_('Name'),
    )

    description = models.CharField(
        max_length=4000,
        verbose_name=_('Description'),
    )

    value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Value'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('User'),
        help_text=_("The item belongs to that user if related.")
    )

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return '{0.name} - {0.currency.sign} {0.value}'.format(self)

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


@python_2_unicode_compatible
class PaymentTransaction(models.Model):
    """
    This model holds the information about a payment transaction.

    Needed in the process of the payment as well as later reference.

    :user: The user this transaction is related to.
    :creation_date: The date this transaction was created.
    :date: The date this transaction was saved last time.
    :transaction_id: The unique identifier of the transaction generated by
      PayPal.
    :value: The amount of the payment. Currency defaults to USD.
    :status: The status of the transaction.

    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        blank=True, null=True,
    )

    object_id = models.PositiveIntegerField(
        blank=True, null=True,
    )

    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation time'),
        blank=True, null=True,
    )

    date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Time'),
    )

    transaction_id = models.CharField(
        max_length=32,
        verbose_name=_('Transaction ID'),
    )

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_('Transaction value'),
    )

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        verbose_name=_('Payment status'),
    )

    completed = models.BooleanField(verbose_name=_("Completed"),
                                    default=False)
    
    class Meta:
        ordering = ['-creation_date', 'transaction_id', ]
        verbose_name = _("Payment transaction")
        verbose_name_plural = _("Payment transactions")

    def __str__(self):
        return self.transaction_id


@python_2_unicode_compatible
class PurchasedItem(models.Model):
    """
    Keeps track of which user purchased which items (and their quantities).

    This helps you to find out if and what your users have purchased.

    :user: FK to the user who made the purchase.
    :identifier: An identifier to select items of the same type. This can be
      helpful if you want to calculate the total shipping costs and the total
      cost of goods for a certain transaction.
    :transaction: The transaction that belongs to this purchase
    :content_object: Use this if you would like to point at any kind of item
      and not the Item model of this app.
    :item: The item that belongs to this purchase
    :price: The price of the item at the time of the purchase
    :quantity: The quantity of items that has been purchased

    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )

    identifier = models.CharField(
        max_length=256,
        verbose_name=_('Identifier'),
        blank=True,
    )

    transaction = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.CASCADE,
        verbose_name=_('Transaction'),
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name=_('Item'),
        null=True, blank=True,
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        blank=True, null=True,
    )

    object_id = models.PositiveIntegerField(
        blank=True, null=True,
    )

    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    price = models.FloatField(
        verbose_name=_('Price'),
        blank=True, null=True,
    )

    quantity = models.PositiveIntegerField(
        verbose_name=_('Quantity'),
    )

    class Meta:
        ordering = ['-transaction__date', 'transaction__transaction_id', ]
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    def __str__(self):
        return u'{0} {1} of {2} [{3}]'.format(
            self.quantity, self.item, self.user.email, self.transaction)


@python_2_unicode_compatible
class PaymentTransactionError(models.Model):
    """
    A model to track errors during payment process.

    :date: When the error occurred.
    :user: For which user the error occurred.
    :paypal_api_url: The API endpoint we have been calling, which has responded
      with the error.
    :request_data: The data payload we have been sending to the API endpoint.
    :response: The full response string from PayPal.
    :transaction: If we send a request at a point in time where we already have
      a transaction, we can add a FK to that transaction for easier cross
      referencing.

    """
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Time'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )

    paypal_api_url = models.CharField(
        max_length=4000,
        verbose_name=_('Paypal API URL'),
        blank=True,
    )

    request_data = models.TextField(
        verbose_name=_('Request data'),
        blank=True,
    )

    response = models.TextField(
        verbose_name=_('Response String'),
        blank=True,
    )

    transaction = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('Payment transaction'),
    )

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = _("Payment transaction error")
        verbose_name_plural = _("Payment transaction errors")
