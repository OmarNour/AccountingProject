from django.contrib.auth.forms import forms
from django.forms import widgets, inlineformset_factory

from tax.models import Tax, TaxComponents
from chart_of_accounts.models import ChartOfAccount


class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ('tax_id',
                  'tax_desc',
                  'tax_account'
                  )

    def __init__(self, *args, **kwargs):
        self.url_org_id = kwargs.pop('org_id')
        super().__init__(*args, **kwargs)
        self.fields['tax_id'].label = 'ID'
        self.fields['tax_desc'].label = 'Desc.'
        tax_accounts = ChartOfAccount.objects.filter(org_id=self.url_org_id, type_code=2).order_by('type_code', 'name')
        self.fields['tax_account'] = forms.ModelChoiceField(queryset=tax_accounts,
                                                            required=True,
                                                            label='Account',
                                                            widget=widgets.Select(attrs={'size': 1}))


class TaxComponentForm(forms.ModelForm):
    class Meta:
        model = TaxComponents
        fields = ('component_desc',
                  'percentage',
                  'compound'
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['component_desc'].label = ''
        self.fields['percentage'].label = ''
        self.fields['compound'] = forms.BooleanField(required=False,
                                                     label='',
                                                     initial=False)

    # def clean_compound(self):
    #     data = self.cleaned_data
    #     print(self.cleaned_data.get('compound'))
    #
    #     x = 0
    #     if self.cleaned_data.get('compound'):
    #         x += 1
    #
    #     print(x)
    #     raise forms.ValidationError("Dr and Cr Accounts are Not Balanced!")
    #     return data.get('compound')


TaxComponentFormSet = inlineformset_factory(Tax, TaxComponents, form=TaxComponentForm, extra=5, min_num=1, validate_min=True)

