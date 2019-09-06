# Generated by Django 2.2.4 on 2019-08-08 10:28

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='HouseholdGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Stationery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('vendor_code', models.CharField(blank=True, max_length=64)),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('KZT', 'Tenge')], default='KZT', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(decimal_places=4, default_currency='KZT', max_digits=19)),
                ('image', models.ImageField(blank=True, null=True, upload_to='stationeries/%Y/%m/%d')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='goods.Category')),
            ],
        ),
    ]