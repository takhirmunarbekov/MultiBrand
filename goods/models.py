from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import (
    ValidationError,
    MaxValueValidator,
    MinValueValidator,
)
from ordered_model.models import OrderedModel
from djmoney.models.fields import MoneyField
from markupfield.fields import MarkupField


# Create your models here.


class Category(OrderedModel):
    
    of = models.ForeignKey(to='self',
        related_name='subcategories',
        blank=True, null=True,
        on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    order_with_respect_to = 'of'

    class Meta(OrderedModel.Meta):
        
        pass

    def clean(self, *args, **kwargs):
        visited = set()
        category = self
        while category is not None:
            if category.id in visited:
                raise ValidationError("Found recursive cycle!")
            visited.add(category.id)
            category = category.of
        super(Category, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Item(models.Model):

    UNIT_CHOICES = (
        ('кор.', 'Коробка'),
        ('рул.', 'Рулон'),
        ('упак.', 'Упаковка'),
        ('лист', 'Лист'),
        ('кг.', 'Килограмм'),
        ('бут.', 'Бутылка'),
        ('бан.', 'Банка'),
        ('пач.', 'Пачка'),
        ('бобина', 'Бобина'),
        ('пара', 'Пара'),
        ('комплект', 'Комплект'),
        ('м.', 'Метр'),
        ('шт.', 'Штук'),
        ('м.п.', 'Погонный метр'),
    )

    category = models.ForeignKey(to=Category,
        related_name='items',
        blank=True, null=True,
        on_delete=models.SET_NULL)
    vendor_code = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    description = models.TextField(blank=True)
    body = MarkupField()
    amount = models.IntegerField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    image = models.ImageField(upload_to='items/%Y/%m/%d', null=True, blank=True)
    price = MoneyField(max_digits=19, decimal_places=2, default_currency='KZT')

    is_new = models.BooleanField(default=False)
    is_hit = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ('-created',)

    def __str__(self):
        return self.name


class Stock(models.Model):
    
    item = models.OneToOneField(to=Item,
        related_name='stock', on_delete=models.CASCADE)
    percent = models.FloatField(validators=[
        MinValueValidator(0),
        MaxValueValidator(1),
    ])
    start = models.DateTimeField()
    end = models.DateTimeField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ('-created',)

    def __str__(self):
        return self.item


class Feedback(models.Model):

    item = models.ForeignKey(to=Item,
        related_name='feedbacks', on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(),
        related_name='feedbacks', on_delete=models.CASCADE)
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ('-created',)

    def __str__(self):
        return self.user


class Rating(models.Model):

    item = models.ForeignKey(to=Item,
        related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(),
        related_name='ratings', on_delete=models.CASCADE)
    rate = models.FloatField(validators=[
        MinValueValidator(0),
        MaxValueValidator(1),
    ])

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:

        unique_together = (
            'item', 'user',
        )


class Like(models.Model):

    item = models.ForeignKey(to=Item,
        related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(),
        related_name='likes', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = (
            'item', 'user',
        )
    
    