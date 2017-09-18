# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-17 14:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AccountingApp', '0002_auto_20170917_1606'),
        ('bill', '0005_billdetails_amounts_are'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billdetails',
            name='amounts_are',
        ),
        migrations.AddField(
            model_name='bill',
            name='amounts_are',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='BillDetails_amounts_are_LOV', to='AccountingApp.LOV'),
            preserve_default=False,
        ),
    ]
