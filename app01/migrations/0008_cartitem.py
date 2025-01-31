# Generated by Django 5.0.7 on 2024-10-21 06:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_logininformation_username_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart_commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='app01.commodityinformation')),
                ('cart_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='app01.logininformation')),
            ],
        ),
    ]
