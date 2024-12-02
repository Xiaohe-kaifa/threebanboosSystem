# Generated by Django 5.0.7 on 2024-10-10 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_ordersinformation_alter_logininformation_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordersinformation',
            name='commodityIntroduce',
        ),
        migrations.RemoveField(
            model_name='ordersinformation',
            name='commodityName',
        ),
        migrations.RemoveField(
            model_name='ordersinformation',
            name='commodityOther',
        ),
        migrations.RemoveField(
            model_name='ordersinformation',
            name='commodityPhoto',
        ),
        migrations.RemoveField(
            model_name='ordersinformation',
            name='commodityPriceAfter',
        ),
        migrations.RemoveField(
            model_name='ordersinformation',
            name='commodityPriceBefore',
        ),
        migrations.RemoveField(
            model_name='ordersinformation',
            name='commodityShopName',
        ),
        migrations.RemoveField(
            model_name='ordersinformation',
            name='commodityShopNumber',
        ),
        migrations.AlterField(
            model_name='ordersinformation',
            name='order_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='下单时间'),
        ),
    ]
