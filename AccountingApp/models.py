from django.db import models
from django.utils import timezone


class Sign(models.Model):
    sign = models.CharField(max_length=1, primary_key=True)

    def __str__(self):
        return self.sign


class DrCr(models.Model):
    dr_cr_id = models.IntegerField(primary_key=True)
    dr_cr_desc = models.CharField(max_length=2, null=False,blank=False)

    def __str__(self):
        return '{} - {}'.format(self.dr_cr_id,self.dr_cr_desc)


class AccountTypes(models.Model):
    # Assets = Liabilities + Equity/Capital + Income/Revenue - Expenses
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=500)
    main_code = models.ForeignKey('self',null=True,blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class AccountTypesDrCr(models.Model):
    # Assets = Liabilities + Equity/Capital + Income/Revenue - Expenses
    code = models.ForeignKey(AccountTypes)
    dr_cr = models.ForeignKey(DrCr, null=False, blank=False)
    sign = models.ForeignKey(Sign, null=False, blank=False)

    class Meta:
        unique_together = ('code', 'dr_cr')

    def __str__(self):
        return '{} {} {}'.format(self.code, self.dr_cr, self.sign)


class ChartOfAccounts(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=500)
    type_code = models.ForeignKey(AccountTypes)
    main_code = models.ForeignKey('self', null=True, blank=True)

    def related_transactions(self):
        return self.Transactions_cr_account_code()

    def __str__(self):
        return '{} - {}'.format(self.name, self.type_code)


class Currencies(models.Model):
    currency_id = models.CharField(primary_key=True, max_length=4)
    decimal_precision = models.IntegerField(default=2, null=False,blank=False)
    currency_latin_name = models.CharField(max_length=500)
    currency_arabic_name = models.CharField(max_length=500)
    base_currency = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.currency_id, '(Base)' if self.base_currency else '')


class Transactions(models.Model):
    transaction_id = models.IntegerField(primary_key=True, null=False,blank=False)
    transaction_date = models.DateTimeField(default=timezone.now(), null=False,blank=False)
    value_date = models.DateTimeField(default=timezone.now(), null=False,blank=False)
    amount = models.DecimalField(max_digits=30, decimal_places=6, default=0, null=False, blank=False)
    dr_account_code = models.ForeignKey(ChartOfAccounts, null=True, blank=False, related_name='Transactions_dr_account_code')
    cr_account_code = models.ForeignKey(ChartOfAccounts, null=True, blank=False, related_name='Transactions_cr_account_code')
    currency_id = models.ForeignKey(Currencies, null=False,blank=False, related_name='Transactions_currency_id')
    base_currency_id = models.ForeignKey(Currencies, null=False, blank=False, related_name='Transactions_base_currency_id')
    exchange_rate = models.DecimalField(max_digits=30, decimal_places=6, null=False,blank=False)
    base_eqv_amount = models.DecimalField(max_digits=30, decimal_places=6, default=0, null=False, blank=False)
    narrative = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return '{} {} ({}) ({})'.format(self.transaction_id, self.amount, self.dr_account_code, self.cr_account_code)


class ExchangeRate(models.Model):
    exchange_rate_id = models.AutoField(primary_key=True)
    from_currency_id = models.ForeignKey(Currencies, related_name='from_currency_id', null=False, blank=False)
    to_currency_id = models.ForeignKey(Currencies, related_name='to_currency_id', null=False, blank=False)
    rate = models.DecimalField(max_digits=30, decimal_places=6, null=False, blank=False)
    override_rate = models.DecimalField(max_digits=30, decimal_places=6, default=0, null=False, blank=False)
    last_updated = models.DateTimeField(default=timezone.now(), null=False, blank=False)

    class Meta:
        unique_together = ('from_currency_id', 'to_currency_id')

    def __str__(self):
        return '{} To {}: {}'.format(self.from_currency_id, self.to_currency_id,self.override_rate if self.override_rate > 0 else self.rate)


class ContactUs(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=500)
    message = models.TextField(max_length=4000)

    def __str__(self):
        return self.email


