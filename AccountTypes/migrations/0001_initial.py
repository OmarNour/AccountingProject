# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-17 11:38
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0007_auto_20170815_2219'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('name', models.CharField(max_length=500, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created_by', models.ForeignKey(default=django.contrib.auth.models.User, on_delete=django.db.models.deletion.CASCADE, related_name='accountType_created_by', to=settings.AUTH_USER_MODEL)),
                ('main_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AccountTypes.AccountTypes')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accountType_modified_by', to=settings.AUTH_USER_MODEL)),
                ('org_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountType_org_id', to='organizations.Organization')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='accounttypes',
            unique_together=set([('org_id', 'code')]),
        ),
    ]