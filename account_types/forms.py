from django.forms import widgets

from AccountingApp.models import Sign
from .models import AccountType
from django.contrib.auth.forms import forms


class CreateAccountTypeForm(forms.ModelForm):
    class Meta:
        model = AccountType
        fields = ('id', 'code', 'name', 'dr_sign', 'cr_sign', 'main_code')

    def __init__(self, *args, **kwargs):

        # self.fields["username"].label = "Display name"
        # self.fields["email"].label = "Email address"
        signs = Sign.objects.all()
        related_account_types = AccountType.objects.filter(org_id=kwargs.pop('org_id'))
        super().__init__(*args, **kwargs)
        self.fields['dr_sign'] = forms.ModelChoiceField(queryset=signs,
                                                        required=True,
                                                        widget=widgets.Select(attrs={'size': 1}))
        self.fields['cr_sign'] = forms.ModelChoiceField(queryset=signs,
                                                        required=True,
                                                        widget=widgets.Select(attrs={'size': 1}))

        self.fields['main_code'] = forms.ModelChoiceField(queryset=related_account_types,
                                                          required=False,
                                                          widget=widgets.Select(attrs={'size': 1}))

        self.fields['main_code'] = forms.ModelChoiceField(queryset=related_account_types,
                                                          required=False,
                                                          widget=widgets.Select(attrs={'size': 1}))


class UpdateAccountTypeForm(forms.ModelForm):
    class Meta:
        model = AccountType
        fields = ('id', 'code', 'name', 'dr_sign', 'cr_sign', 'main_code')

    def __init__(self, *args, **kwargs):

        # self.fields["username"].label = "Display name"
        # self.fields["email"].label = "Email address"
        signs = Sign.objects.all()
        related_account_types = AccountType.objects.filter(org_id=kwargs.pop('org_id')).exclude(code=kwargs.pop('acc_typ_code'))
        super().__init__(*args, **kwargs)
        self.fields['dr_sign'] = forms.ModelChoiceField(queryset=signs,
                                                        required=True,
                                                        widget=widgets.Select(attrs={'size': 1}))
        self.fields['cr_sign'] = forms.ModelChoiceField(queryset=signs,
                                                        required=True,
                                                        widget=widgets.Select(attrs={'size': 1}))

        self.fields['main_code'] = forms.ModelChoiceField(queryset=related_account_types,
                                                          required=False,
                                                          widget=widgets.Select(attrs={'size': 1}))

