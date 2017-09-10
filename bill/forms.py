from django.contrib.auth.forms import forms
from django.forms import widgets, inlineformset_factory

from bill.models import Bill, BillDetails
from organizations.models import OrgCurrencies
from purchase_order.models import PurchaseOrder
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
                  )

    def __init__(self, *args, **kwargs):
        self.url_org_id = kwargs.pop('org_id')
        super().__init__(*args, **kwargs)
        po_numbers = PurchaseOrder.objects.filter(org_id=self.url_org_id).order_by('po_number')
        vendors = Vendor.objects.filter(org_id=self.url_org_id).order_by('name')
        org_currencies = OrgCurrencies.objects.filter(Org_id=self.url_org_id).order_by('currency_id')
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


class BillDetailsForm(forms.ModelForm):
    class Meta:
        model = BillDetails
        fields = ('item',
                  'description',
                  'qty',
                  'unit_price',
                  'amount',
                  'dr_account',
                  'cr_account'
                  )

    def __init__(self, *args, **kwargs):
        self.url_org_id = kwargs.pop('org_id') # how can i get the org ID
        super().__init__(*args, **kwargs)
        print(self.url_org_id)
        self.fields['item'].label = ''
        self.fields['description'].label = ''
        self.fields['qty'].label = ''
        self.fields['unit_price'].label = ''
        self.fields['amount'].label = ''
        self.fields['dr_account'].label = ''
        self.fields['cr_account'].label = ''


BillDetailsFormSet = inlineformset_factory(Bill, BillDetails, form=BillDetailsForm, extra=5)

