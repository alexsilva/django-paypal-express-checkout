"""The models for the ``paypal_express_checkout`` app."""
from django.db import models
from django.utils.translation import ugettext_lazy as _

from paypal_express_checkout.constants import STATUS_CHOICES


class Item(models.Model):
    """
    Holds the information about an item, that is on Sale.

    The information will be needed to process the PayPal payment transaction.

    :name: Name of the item.
    :description: Description of the item.
    :value: The price of the item.

    """
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

    def __unicode__(self):
        return '{0} - {1} $'.format(self.name, self.value)


class PaymentTransaction(models.Model):
    """
    This model holds the information about a payment transaction.

    Needed in the process of the payment as well as later reference.

    :user: The user this transaction is related to.
    :date: The date this transaction has started.
    :transaction_id: The unique identifier of the transaction generated by
      PayPal.
    :value: The amount of the payment. Currency defaults to USD.
    :status: The status of the transaction.

    """
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
    )

    date = models.DateTimeField(
        auto_now=True,
        auto_now_add=True,
        verbose_name=_('Time'),
    )

    transaction_id = models.CharField(
        max_length=32,
        verbose_name=_('Transaction ID'),
    )

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


class PaymentTransactionError(models.Model):
    """
    A model to track errors during payment process.

    :data: When the error ocurred.
    :user: For which user the error occurred.
    :response: The full response string from PayPal.

    """
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Time'),
    )

    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('User'),
    )

    response = models.TextField(
        verbose_name=_('Response String'),
    )

    transaction = models.ForeignKey(
        PaymentTransaction,
        blank=True, null=True,
        verbose_name=_('Payment transaction'),
    ),
