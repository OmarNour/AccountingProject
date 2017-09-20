# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-20 08:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AccountingApp', '0003_auto_20170917_2022'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount_is',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Transaction_amount_is_LOV', to='AccountingApp.LOV'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='tax_amount',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=30),
            preserve_default=False,
        ),
    ]
