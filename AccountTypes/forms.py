from .models import AccountTypes
from django.contrib.auth.forms import forms


class CreateAccountTypeForm(forms.ModelForm):
    class Meta:
        model = AccountTypes
        fields = ('id', 'code', 'name', 'main_code')

    def __init__(self, *args, **kwargs):

        # self.fields["username"].label = "Display name"
        # self.fields["email"].label = "Email address"

        related_account_types = AccountTypes.objects.filter(org_id=kwargs.pop('org_id'))
        super().__init__(*args, **kwargs)
        self.fields['main_code'] = forms.ModelChoiceField(queryset=related_account_types, required=False)


class UpdateAccountTypeForm(forms.ModelForm):
    class Meta:
        model = AccountTypes
        fields = ('id', 'code', 'name', 'main_code')

    def __init__(self, *args, **kwargs):

        # self.fields["username"].label = "Display name"
        # self.fields["email"].label = "Email address"

        related_account_types = AccountTypes.objects.filter(org_id=kwargs.pop('org_id')).exclude(code=kwargs.pop('acc_typ_code'))
        super().__init__(*args, **kwargs)
        self.fields['main_code'] = forms.ModelChoiceField(queryset=related_account_types, required=False)

