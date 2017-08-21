# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-15 16:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_auto_20170813_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationmember',
            name='organization_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.ProtectedError, related_name='OrganizationMember_organization_id', to='organizations.Organization'),
        ),
    ]