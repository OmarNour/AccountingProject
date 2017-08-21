from AccountTypes.models import AccountTypes
from .models import ChartOfAccounts
from django.contrib.auth.forms import forms


class CreateChartOfAccountForm(forms.ModelForm):
    class Meta:
        model = ChartOfAccounts
        fields = ('id', 'code', 'name', 'main_code')

    def __init__(self, *args, **kwargs):

        # self.fields["username"].label = "Display name"
        # self.fields["email"].label = "Email address"
        # x = kwargs.pop('acc_typ_code_q2')
        # related_account_types = AccountTypes.objects.filter(org_id=kwargs.pop('org_id_q1'))
        related_chart_of_accounts = ChartOfAccounts.objects.filter(type_code=kwargs.pop('acc_typ_code_id'))
        super().__init__(*args, **kwargs)
        self.fields['main_code'] = forms.ModelChoiceField(queryset=related_chart_of_accounts, required=False)


class UpdateChartOfAccountForm(forms.ModelForm):
    class Meta:
        model = ChartOfAccounts
        fields = ('id', 'code', 'name', 'main_code')

    def __init__(self, *args, **kwargs):

        # self.fields["username"].label = "Display name"
        # self.fields["email"].label = "Email address"
        # x = kwargs.pop('acc_typ_code_q2')
        # related_account_types = AccountTypes.objects.filter(org_id=kwargs.pop('org_id_q1'))
        related_chart_of_accounts = ChartOfAccounts.objects.filter(type_code=kwargs.pop('acc_typ_code_id')).\
                                                            exclude(id=kwargs.pop('account_id'))
        super().__init__(*args, **kwargs)
        self.fields['main_code'] = forms.ModelChoiceField(queryset=related_chart_of_accounts, required=False)

