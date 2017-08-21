# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-13 16:00
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='created_by',
            field=models.ForeignKey(default=django.contrib.auth.models.User, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='organization_created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
