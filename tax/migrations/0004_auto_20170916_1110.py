# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-16 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tax', '0003_auto_20170916_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tax',
            name='total_tax_pct',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
        ),
    ]