# Generated by Django 5.0.7 on 2024-10-16 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_alter_ordersinformation_order_people_account_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='logininformation',
            name='username_type',
            field=models.SmallIntegerField(choices=[(0, '管理员'), (1, '用户'), (2, '商家'), (3, '客服')], default=1, verbose_name='状态'),
        ),
    ]
