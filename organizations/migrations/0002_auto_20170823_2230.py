# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-23 19:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('override_rate', models.DecimalField(decimal_places=6, default=0, max_digits=30)),
                ('last_updated', models.DateTimeField(default=datetime.datetime(2017, 8, 23, 19, 30, 26, 770962, tzinfo=utc))),
                ('Org_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrgExchangeRate_Org_id', to='organizations.Organization')),
                ('from_currency_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrgExchangeRate_from_currency_id', to='organizations.OrgCurrencies')),
                ('related_OrgCurrencies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrgExchangeRate_related_curr_id', to='organizations.OrgCurrencies')),
                ('to_currency_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrgExchangeRate_to_currency_id', to='organizations.OrgCurrencies')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='orgexchangerate',
            unique_together=set([('Org_id', 'related_OrgCurrencies')]),
        ),
    ]