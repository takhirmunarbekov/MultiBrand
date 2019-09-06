from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField

from goods.models import (
    Item,
)

# Create your models here.


class City(models.Model):

    name = models.CharField(max_length=64)


class Region(models.Model):

    city = models.ForeignKey(to=City,
        related_name='regions',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=64)


class Order(models.Model):

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('accepted', 'Accepted'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_CHOICES = (
        ('in cash', 'In cash'),
        ('card', 'Card'),
    )

    user = models.ForeignKey(to=get_user_model(),
        related_name='orders',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    
    city = models.CharField(max_length=64)
    region = models.CharField(max_length=64)
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    email = models.EmailField()
    comment = models.TextField()
    payment = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def is_paid(self):
        transaction = self.transaction
        return transaction is not None \
            and transaction.status == 'accepted'


class ItemOrder(models.Model):

    order = models.ForeignKey(to=Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(to=Item,
        related_name='ordered',
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    vendor_code = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    unit = models.CharField(max_length=10, choices=Item.UNIT_CHOICES)
    price = MoneyField(
        max_digits=19,
        decimal_places=2,
        default_currency='KZT'
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class OrderTransaction(models.Model):

    STATUS_CHOICES = (
        ('accepted', 'Accepted'),
        ('cancelled', 'Cancelled'),
    )
    
    transaction_id = models.PositiveIntegerField(blank=True, null=True)
    order = models.OneToOneField(to=Order,
        related_name='transaction',
        on_delete=models.CASCADE)
    amount = MoneyField(
        max_digits=19,
        decimal_places=2,
        default_currency='KZT'
    )
    status = models.CharField(max_length=10,
        blank=True,
        null=True,
        default=None,
        choices=STATUS_CHOICES)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
