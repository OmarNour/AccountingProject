# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-27 09:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AccountingApp', '0005_auto_20170826_1624'),
        ('AccountTypes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttypes',
            name='cr_sign',
            field=models.ForeignKey(default='+', on_delete=django.db.models.deletion.CASCADE, related_name='account_type_cr_sign', to='AccountingApp.Sign'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accounttypes',
            name='dr_sign',
            field=models.ForeignKey(default='+', on_delete=django.db.models.deletion.CASCADE, related_name='account_type_dr_sign', to='AccountingApp.Sign'),
            preserve_default=False,
        ),
    ]
