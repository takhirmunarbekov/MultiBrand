# Generated by Django 2.2.4 on 2019-09-01 18:05

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.PositiveIntegerField(blank=True, null=True)),
                ('amount_currency', djmoney.models.fields.CurrencyField(choices=[('KZT', 'Tenge')], default='KZT', editable=False, max_length=3)),
                ('amount', djmoney.models.fields.MoneyField(decimal_places=2, default_currency='KZT', max_digits=19)),
                ('status', models.CharField(blank=True, choices=[('accepted', 'Accepted'), ('cancelled', 'Cancelled')], default=None, max_length=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='transaction',
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('in cash', 'In cash'), ('card', 'Card')], default='in cash', max_length=10),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
        migrations.AddField(
            model_name='ordertransaction',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='orders.Order'),
        ),
    ]