from account_types.models import AccountType
from .models import ChartOfAccount
from django.contrib.auth.forms import forms


class CreateChartOfAccountForm(forms.ModelForm):
    class Meta:
        model = ChartOfAccount
        fields = ('id', 'code', 'name', 'main_code')

    def __init__(self, *args, **kwargs):

        # self.fields["username"].label = "Display name"
        # self.fields["email"].label = "Email address"
        # x = kwargs.pop('acc_typ_code_q2')
        # related_account_types = account_types.objects.filter(org_id=kwargs.pop('org_id_q1'))
        related_chart_of_accounts = ChartOfAccount.objects.filter(type_code=kwargs.pop('acc_typ_code_id'))
        super().__init__(*args, **kwargs)
        self.fields['main_code'] = forms.ModelChoiceField(queryset=related_chart_of_accounts, required=False)


class UpdateChartOfAccountForm(forms.ModelForm):
    class Meta:
        model = ChartOfAccount
        fields = ('id', 'code', 'name', 'main_code')

    def __init__(self, *args, **kwargs):

        # self.fields["username"].label = "Display name"
        # self.fields["email"].label = "Email address"
        # x = kwargs.pop('acc_typ_code_q2')
        # related_account_types = account_types.objects.filter(org_id=kwargs.pop('org_id_q1'))
        related_chart_of_accounts = ChartOfAccount.objects.filter(type_code=kwargs.pop('acc_typ_code_id')).\
                                                            exclude(id=kwargs.pop('account_id'))
        super().__init__(*args, **kwargs)
        self.fields['main_code'] = forms.ModelChoiceField(queryset=related_chart_of_accounts, required=False)

