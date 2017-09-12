# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-11 18:31
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('chart_of_accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AccountingApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.IntegerField()),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('value_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=6, default=0, max_digits=30)),
                ('exchange_rate', models.DecimalField(decimal_places=6, max_digits=30)),
                ('base_eqv_amount', models.DecimalField(decimal_places=6, default=0, max_digits=30)),
                ('narrative', models.CharField(max_length=500)),
                ('void', models.BooleanField(default=False)),
                ('reference_number', models.CharField(blank=True, max_length=10, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('base_currency_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Transactions_base_currency_id', to='organizations.OrgCurrencies')),
                ('cr_account_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Transactions_cr_account_code', to='chart_of_accounts.ChartOfAccount')),
                ('created_by', models.ForeignKey(default=django.contrib.auth.models.User, on_delete=django.db.models.deletion.PROTECT, related_name='Transactions_created_by', to=settings.AUTH_USER_MODEL)),
                ('currency_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Transactions_currency_id', to='organizations.OrgCurrencies')),
                ('dr_account_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Transactions_dr_account_code', to='chart_of_accounts.ChartOfAccount')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Transactions_modified_by', to=settings.AUTH_USER_MODEL)),
                ('org_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Transactions_org_id', to='organizations.Organization')),
                ('transaction_source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Transactions_source', to='AccountingApp.TransactionSources')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together=set([('org_id', 'transaction_id')]),
        ),
    ]
