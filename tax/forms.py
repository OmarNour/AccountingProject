from django.contrib.auth import get_user_model
from django.contrib.auth.forms import forms
from django.forms import widgets, inlineformset_factory
from django.utils import timezone

from tax.models import Tax, TaxComponents
from chart_of_accounts.models import ChartOfAccount
User = get_user_model()


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
                  'compound',
                  # 'created_by'
                  # 'modified_by',
                  # 'updated_date'
                  )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # self.fields['created_by'] = forms.CharField(required=False,
        #                                             label='',
        #                                             initial=False,
        #                                             widget=forms.HiddenInput())
        self.fields['component_desc'].label = ''
        self.fields['percentage'].label = ''
        self.fields['compound'] = forms.BooleanField(required=False,
                                                     label='',
                                                     initial=False)



        # self.fields['modified_by'] = forms.CharField(required=False,
        #                                                 label='',
        #                                                 initial=False,
        #                                                 widget=forms.HiddenInput())
        #
        # self.fields['updated_date'] = forms.DateTimeField(required=False,
        #                                                  label='',
        #                                                  initial=False,
        #                                                  widget=forms.HiddenInput())

    # def clean_created_by(self):
    #     data = self.cleaned_data
    #     # print(self.cleaned_data['created_by'])
    #     self.cleaned_data['created_by'] = self.user
    #     # if self.cleaned_data['created_by']:
    #     #     print('pass')
    #     #     pass
    #     # else:
    #     #     print('assign')
    #     #     self.cleaned_data['created_by'] = self.user
    #     return data.get('created_by')

    # def clean_updated_date(self):
    #     data = self.cleaned_data
    #     if self.cleaned_data['updated_date']:
    #         pass
    #     else:
    #         self.cleaned_data['updated_date'] = timezone.datetime.now()
    #     return data.get('updated_date')


TaxComponentFormSet = inlineformset_factory(Tax, TaxComponents, form=TaxComponentForm, extra=5, min_num=1, validate_min=True)

