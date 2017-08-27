from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from AccountingApp.models import TransactionSources
from chart_of_accounts.models import ChartOfAccounts
from organizations.models import OrgCurrencies, Organization

User = get_user_model()


class Transaction(models.Model):
    org_id = models.ForeignKey(Organization, null=False,blank=False,related_name='Transactions_org_id')
    transaction_id = models.IntegerField(null=False,blank=False)
    transaction_date = models.DateTimeField(default=timezone.now, null=False,blank=False)
    value_date = models.DateTimeField(default=timezone.now, null=False,blank=False)
    amount = models.DecimalField(max_digits=30, decimal_places=6, default=0, null=False, blank=False)
    dr_account_code = models.ForeignKey(ChartOfAccounts, null=True, blank=False, related_name='Transactions_dr_account_code')
    cr_account_code = models.ForeignKey(ChartOfAccounts, null=True, blank=False, related_name='Transactions_cr_account_code')
    currency_id = models.ForeignKey(OrgCurrencies, null=False,blank=False, related_name='Transactions_currency_id')
    base_currency_id = models.ForeignKey(OrgCurrencies, null=False, blank=False, related_name='Transactions_base_currency_id')
    exchange_rate = models.DecimalField(max_digits=30, decimal_places=6, null=False,blank=False)
    base_eqv_amount = models.DecimalField(max_digits=30, decimal_places=6, default=0, null=False, blank=False)
    narrative = models.CharField(max_length=500, null=True, blank=True)
    void = models.BooleanField(default=False)
    transaction_source = models.ForeignKey(TransactionSources, null=False,blank=False, related_name='Transactions_source')

    created_by = models.ForeignKey(User, default=User, related_name='Transactions_created_by')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.ForeignKey(User, null=True, blank=True, related_name='Transactions_modified_by')
    updated_date = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        unique_together = ('org_id', 'transaction_id')

    def __str__(self):
        return '{} {} ({}) ({})'.format(self.transaction_id, self.amount, self.dr_account_code, self.cr_account_code)
