# Generated by Django 2.2.4 on 2019-08-26 16:26

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0009_auto_20190808_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='of',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategories', to='goods.Category'),
        ),
        migrations.AddField(
            model_name='item',
            name='amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='desc',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='is_hit',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.CharField(choices=[('кор.', 'Коробка'), ('рул.', 'Рулон'), ('упак.', 'Упаковка'), ('лист', 'Лист'), ('кг.', 'Килограмм'), ('бут.', 'Бутылка'), ('бан.', 'Банка'), ('пач.', 'Пачка'), ('бобина', 'Бобина'), ('пара', 'Пара'), ('комплект', 'Комплект'), ('м.', 'Метр'), ('шт.', 'Штук'), ('м.п.', 'Погонный метр')], default='шт.', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='goods.Category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='items/%Y/%m/%d'),
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='goods.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='goods.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feebacks', to='goods.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feebacks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
