from django.contrib.auth.forms import forms
from django.forms import widgets, inlineformset_factory

from AccountingApp.models import LOV
from bill.models import Bill, BillDetails
from chart_of_accounts.models import ChartOfAccount
from inventory.models import Inventory
from organizations.models import OrgCurrencies
from purchase_order.models import PurchaseOrder
from tax.models import Tax
from transactions.views import valid_transaction
from vendor.models import Vendor


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ('bill_no',
                  'po_number',
                  'vendor',
                  'currency',
                  'bill_date',
                  'due_date',
                  'amounts_are'
                  )
#TAX_OPTIONS
    def __init__(self, *args, **kwargs):
        self.url_org_id = kwargs.pop('org_id')
        super().__init__(*args, **kwargs)
        po_numbers = PurchaseOrder.objects.filter(org_id=self.url_org_id).order_by('po_number')
        vendors = Vendor.objects.filter(org_id=self.url_org_id).order_by('name')
        org_currencies = OrgCurrencies.objects.filter(Org_id=self.url_org_id).order_by('currency_id')
        tax_options = LOV.objects.filter(domain='TAX_OPTIONS').order_by('id')
        self.fields['po_number'] = forms.ModelChoiceField(queryset=po_numbers,
                                                          required=False,
                                                          label='PO. #',
                                                          widget=widgets.Select(attrs={'size': 1}))
        self.fields['vendor'] = forms.ModelChoiceField(queryset=vendors,
                                                       required=True,
                                                       label='Vendor',
                                                       widget=widgets.Select(attrs={'size': 1}))
        self.fields['currency'] = forms.ModelChoiceField(queryset=org_currencies,
                                                         required=True,
                                                         label='Currency',
                                                         widget=widgets.Select(attrs={'size': 1}))
        self.fields['bill_date'] = forms.DateField(widget=widgets.SelectDateWidget(attrs={'size': 1}))

        self.fields['due_date'] = forms.DateField(widget=widgets.SelectDateWidget(attrs={'size': 1}))

        self.fields['amounts_are'] = forms.ModelChoiceField(queryset=tax_options,
                                                            required=True,
                                                            label='Amounts are',
                                                            widget=widgets.Select(attrs={'size': 1}))


class BillDetailsForm(forms.ModelForm):
    class Meta:
        model = BillDetails
        fields = ('item',
                  'description',
                  'qty',
                  'unit_price',
                  # 'amount',
                  'dr_account',
                  'cr_account',
                  'tax'
                  )

    def __init__(self, *args, **kwargs):
        self.url_org_id = kwargs.pop('org_id') # how can i get the org ID
        super().__init__(*args, **kwargs)
        # print(self.url_org_id)

        self.fields['item'].label = ''
        self.fields['description'].label = ''
        self.fields['qty'].label = ''
        self.fields['unit_price'].label = ''
        # self.fields['amount'].label = ''
        self.fields['cr_account'].label = ''
        items = Inventory.objects.filter(org_id=self.url_org_id).order_by('item_id')
        self.fields['item'] = forms.ModelChoiceField(queryset=items,
                                                     required=False,
                                                     label='',
                                                     widget=widgets.Select(attrs={'size': 1}))
        dr_accounts = ChartOfAccount.objects.filter(org_id=self.url_org_id).order_by('type_code', 'name')
        cr_accounts = ChartOfAccount.objects.filter(org_id=self.url_org_id).order_by('type_code', 'name')
        self.fields['dr_account'] = forms.ModelChoiceField(queryset=dr_accounts,
                                                           required=True,
                                                           label='',
                                                           widget=widgets.Select(attrs={'size': 1}))
        self.fields['cr_account'] = forms.ModelChoiceField(queryset=cr_accounts,
                                                           required=True,
                                                           label='',
                                                           widget=widgets.Select(attrs={'size': 1}))
        taxes = Tax.objects.filter(org_id=self.url_org_id).order_by('tax_desc')
        self.fields['tax'] = forms.ModelChoiceField(queryset=taxes,
                                                    required=False,
                                                    label='',
                                                    widget=widgets.Select(attrs={'size': 1}))

    def clean_cr_account(self):
        cr_account = self.cleaned_data
        if not valid_transaction(org_id=self.url_org_id,
                                 dr_type_code=self.cleaned_data['dr_account'].type_code.id,
                                 dr_account_code=self.cleaned_data['dr_account'].code,
                                 cr_type_code=self.cleaned_data['cr_account'].type_code.id,
                                 cr_account_code=self.cleaned_data['cr_account'].code):
            raise forms.ValidationError("Dr and Cr Accounts are Not Balanced!")
        return cr_account.get('cr_account')
        # print(self.cleaned_data['description'])
        # raise forms.ValidationError("Items in a set must be distinct.")
    #
    # def clean_tax(self):
    #     tax = self.cleaned_data
    #
    #     return tax.get('tax')


BillDetailsFormSet = inlineformset_factory(Bill, BillDetails, form=BillDetailsForm, extra=5, min_num=1, validate_min=True)

