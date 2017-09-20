from django.forms import widgets

from AccountingApp.models import LOV
from chart_of_accounts.models import ChartOfAccount
from organizations.models import OrgCurrencies
from tax.models import Tax
from transactions import views as trnx_views
from .models import Transaction
from django.contrib.auth.forms import forms


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('id',
                  'amount',
                  'currency_id',
                  'base_currency_id',
                  'dr_account_code',
                  'cr_account_code',
                  'transaction_date',
                  'amount_is',
                  'tax',
                  # 'exchange_rate',
                  # 'base_eqv_amount',

                  'narrative')

    def __init__(self, *args, **kwargs):
        self.url_org_id = kwargs.pop('org_id')
        super().__init__(*args, **kwargs)

        org_accounts = ChartOfAccount.objects.filter(org_id=self.url_org_id).order_by('type_code')
        org_currencies = OrgCurrencies.objects.filter(Org_id=self.url_org_id).order_by('currency_id')
        base_currency = OrgCurrencies.objects.filter(Org_id=self.url_org_id, base_currency=True).order_by('currency_id')

        self.fields['dr_account_code'] = forms.ModelChoiceField(queryset=org_accounts,
                                                                required=True,
                                                                label='Dr. Account',
                                                                widget=widgets.Select(attrs={'size': 1}))

        self.fields['cr_account_code'] = forms.ModelChoiceField(queryset=org_accounts,
                                                                required=True,
                                                                label='Cr. Account',
                                                                widget=widgets.Select(attrs={'size': 1}))

        self.fields['currency_id'] = forms.ModelChoiceField(queryset=org_currencies,
                                                            required=True,
                                                            label='Currency',
                                                            widget=widgets.Select(attrs={'size': 1}))

        # print(base_currency.get().currency_id)

        self.fields['base_currency_id'] = forms.ModelChoiceField(queryset=base_currency,
                                                                 required=True,
                                                                 label='Base Currency',
                                                                 initial=base_currency.get().currency_id,
                                                                 widget=widgets.Select(attrs={'size': 1,'readonly':True}),
                                                                 )

        tax_options = LOV.objects.filter(domain='TAX_OPTIONS').order_by('id')
        self.fields['amount_is'] = forms.ModelChoiceField(queryset=tax_options,
                                                          required=True,
                                                          label='Amount is',
                                                          widget=widgets.Select(attrs={'size': 1}))

        taxes = Tax.objects.filter(org_id=self.url_org_id).order_by('tax_desc')
        self.fields['tax'] = forms.ModelChoiceField(queryset=taxes,
                                                    required=False,
                                                    label='Tax',
                                                    widget=widgets.Select(attrs={'size': 1}))

    def clean_amount(self):
        amount = self.cleaned_data
        if self.cleaned_data['amount'] <= 0:
            raise forms.ValidationError("Invalid amount!")
        return amount.get('amount')

    def clean(self):
        # cleaned_data = super(TransactionForm, self).clean()
        if self.cleaned_data['amount_is'].id != 3 and not self.cleaned_data['tax']:
            raise forms.ValidationError("Please select Tax!")

        if not trnx_views.valid_transaction(self.url_org_id,
                                            self.cleaned_data['dr_account_code'].type_code.id,
                                            self.cleaned_data['dr_account_code'].code,
                                            self.cleaned_data['cr_account_code'].type_code.id,
                                            self.cleaned_data['cr_account_code'].code):
            raise forms.ValidationError("Dr and Cr Accounts are Not Balanced!")





