# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-30 23:26
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('account_types', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChartOfAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField()),
                ('name', models.CharField(max_length=500)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created_by', models.ForeignKey(default=django.contrib.auth.models.User, on_delete=django.db.models.deletion.CASCADE, related_name='ChartOfAccounts_created_by', to=settings.AUTH_USER_MODEL)),
                ('main_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ChartOfAccounts_main_code', to='chart_of_accounts.ChartOfAccount')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ChartOfAccounts_modified_by', to=settings.AUTH_USER_MODEL)),
                ('org_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChartOfAccounts_org_id', to='organizations.Organization')),
                ('type_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ChartOfAccounts_type_code', to='account_types.AccountType')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='chartofaccount',
            unique_together=set([('org_id', 'type_code', 'name'), ('org_id', 'type_code', 'code')]),
        ),
    ]
