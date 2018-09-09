# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-06 12:42
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '0001_initial'),
        ('organizations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_number', models.CharField(max_length=10)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('mark_as_billed', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(blank=True, editable=False, null=True)),
                ('created_by', models.ForeignKey(default=django.contrib.auth.models.User, on_delete=django.db.models.deletion.CASCADE, related_name='PurchaseOrder_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='PurchaseOrder_modified_by', to=settings.AUTH_USER_MODEL)),
                ('org_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PurchaseOrder_org_id', to='organizations.Organization')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PurchaseOrder_vendor', to='vendor.Vendor')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase_order.PurchaseOrder')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='purchaseorder',
            unique_together=set([('org_id', 'po_number')]),
        ),
    ]