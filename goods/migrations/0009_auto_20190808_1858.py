# Generated by Django 2.2.4 on 2019-08-08 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0008_auto_20190808_1821'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Stationery',
            new_name='Item',
        ),
        migrations.DeleteModel(
            name='HouseholdGoods',
        ),
        migrations.DeleteModel(
            name='Instrument',
        ),
    ]
