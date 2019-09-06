# Generated by Django 2.2.4 on 2019-08-29 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0014_auto_20190829_1633'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.PositiveIntegerField()),
                ('amount_currency', djmoney.models.fields.CurrencyField(choices=[('KZT', 'Tenge')], default='KZT', editable=False, max_length=3)),
                ('amount', djmoney.models.fields.MoneyField(decimal_places=2, default_currency='KZT', max_digits=19)),
                ('status', models.CharField(blank=True, choices=[('accepted', 'Accepted'), ('refunded', 'Refunded')], default=None, max_length=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='orders.City')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=64)),
                ('region', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.TextField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('accepted', 'Accepted'), ('cancelled', 'Cancelled')], max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('transaction', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order', to='orders.Transaction')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_code', models.CharField(max_length=64, null=True)),
                ('name', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('unit', models.CharField(choices=[('кор.', 'Коробка'), ('рул.', 'Рулон'), ('упак.', 'Упаковка'), ('лист', 'Лист'), ('кг.', 'Килограмм'), ('бут.', 'Бутылка'), ('бан.', 'Банка'), ('пач.', 'Пачка'), ('бобина', 'Бобина'), ('пара', 'Пара'), ('комплект', 'Комплект'), ('м.', 'Метр'), ('шт.', 'Штук'), ('м.п.', 'Погонный метр')], max_length=10)),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('KZT', 'Tenge')], default='KZT', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(decimal_places=2, default_currency='KZT', max_digits=19)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordered', to='goods.Item')),
            ],
        ),
    ]
