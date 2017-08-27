from django import forms
from AccountingApp.models import ContactUs, AccountTypes, ChartOfAccounts,Transactions
from django.contrib.auth.models import User
from AccountingApp import views as AppView
# from django.core import validators


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'


class TransactionsForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = '__all__'

    def clean(self):
        base_currency = AppView.get_base_currency()
        self.cleaned_data['exchange_rate'] = AppView.get_exchange_rate(self.cleaned_data['currency_id'].currency_id,
                                                                     base_currency)

        base_eqv_amount = self.cleaned_data['exchange_rate'] * self.cleaned_data['amount']

        self.cleaned_data['base_currency_id'].currency_id = base_currency
        self.cleaned_data['base_eqv_amount'] = round(base_eqv_amount,6)

        if not AppView.validate_transaction(self.cleaned_data['dr_account_code'].code,
                                            self.cleaned_data['cr_account_code'].code):
            raise forms.ValidationError("Dr and Cr are Not Balanced!")


class AccountTypesForm(forms.ModelForm):
    class Meta:
        model = AccountTypes
        fields = '__all__'


class ChartOfAccountsForm(forms.ModelForm):
    class Meta:
        model = ChartOfAccounts
        fields = '__all__'


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


