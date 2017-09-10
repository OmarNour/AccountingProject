from django.forms import widgets

from AccountingApp.models import Currencies
from organizations import views
from .models import Organization, OrgCurrencies, OrgExchangeRate, InvitedUsers
from django.contrib.auth.forms import forms
from django.core.exceptions import ValidationError


class CreateOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'email')
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


class OrganizationUpdateForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('id','name', 'email')

    # def __init__(self, *args, **kwargs):
    #
    #     # self.fields["username"].label = "Display name"
    #     # self.fields["email"].label = "Email address"
    #
    #     # org_owner = Organization.objects.filter(id=kwargs.pop('org_id')).get().owner
    #     org_owner = Organization.objects.filter(id=kwargs.pop('owner_org_id')).get().owner
    #
    #     related_organizations = Organization.objects.\
    #                             filter(owner=org_owner).\
    #                             exclude(id=kwargs.pop('exclude_org_id'))
    #
    #     super().__init__(*args, **kwargs)
        # self.fields['main_org'] = forms.ModelChoiceField(queryset=related_organizations,
        #                                                  required=False,
        #                                                  widget=widgets.Select(attrs={'size': 1}))


class CurrenciesForm(forms.ModelForm):
    class Meta:
        model = OrgCurrencies
        fields = ('id', 'currency_id', 'decimal_precision', 'base_currency')

    def __init__(self, *args, **kwargs):
        self.org_id = kwargs.pop('org_id')
        super().__init__(*args, **kwargs)
        all_currencies = Currencies.objects.all()
        self.fields['currency_id'] = forms.ModelChoiceField(queryset=all_currencies,
                                                            required=True,
                                                            widget=widgets.Select(attrs={'size': 1}))

        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields["currency_id"].widget = forms.HiddenInput()

    def clean_base_currency(self):
        data = self.cleaned_data
        new_base_currency = False
        base_currency_changed = False
        # print(data.get('currency_id'))

        try:
            OrgCurrencies.objects.filter(Org_id=self.org_id, currency_id=data.get('currency_id')).get()
        except OrgCurrencies.DoesNotExist:
            base_currency_changed = False
            if self.cleaned_data.get('base_currency') is True:
                OrgCurrencies.objects.filter(Org_id=self.org_id).update(base_currency=False)

        else:
            try:
                current_base = OrgCurrencies.objects.filter(Org_id=self.org_id, base_currency=True).get()

            except OrgCurrencies.DoesNotExist:
                # print('DoesNotExist')

                if self.cleaned_data.get('base_currency') is True:
                    OrgCurrencies.objects.filter(Org_id=self.org_id).update(base_currency=False)
                    base_currency_changed = True
                    new_base_currency = True

            else:
                if self.cleaned_data.get('currency_id') == current_base.currency_id \
                        and self.cleaned_data.get('base_currency') is False:
                    new_base_currency = False

                elif self.cleaned_data.get('currency_id') != current_base.currency_id \
                        and self.cleaned_data.get('base_currency') is True:

                    base_currency_changed = True
                    OrgCurrencies.objects.filter(Org_id=self.org_id).update(base_currency=False)
                else:
                    new_base_currency = False

            if base_currency_changed:
                org_id = Organization.objects.filter().get(id=self.org_id)
                views.handle_exchange_rate(org_id=org_id,
                                           from_currency_id=self.cleaned_data.get('currency_id'),
                                           new_base_currency=base_currency_changed)

        # self.cleaned_data['base_currency'] = True
        if self.cleaned_data.get('base_currency') is False and \
                OrgCurrencies.objects.filter(Org_id=self.org_id,
                                             base_currency=True).exclude(currency_id=self.cleaned_data.get('currency_id')).count() == 0:
            self.cleaned_data['base_currency'] = True
        return data.get('base_currency')


class OverrideOrgExchangeRateForm(forms.ModelForm):
    class Meta:
        model = OrgExchangeRate
        fields = ('id', 'swapped_current_rate', 'override_rate')

    def __init__(self, *args, **kwargs):
        self.url_org_id = kwargs.pop('org_id')
        self.url_curr_id = kwargs.pop('curr_id')
        self.url_pk = kwargs.pop('pk')
        super().__init__(*args, **kwargs)
        self.fields["swapped_current_rate"].label = "Current rate"
        self.fields['swapped_current_rate'].widget.attrs['readonly'] = True


class InviteUserForm(forms.ModelForm):
    class Meta:
        model = InvitedUsers
        fields = ('id',
                  'invited_user_first_name',
                  'invited_user_last_name',
                  'invited_user_email')

    def __init__(self, *args, **kwargs):
        self.url_org_id = kwargs.pop('org_id')

        super().__init__(*args, **kwargs)
        self.fields["invited_user_first_name"].label = "First name"
        self.fields["invited_user_last_name"].label = "Last name"
        self.fields["invited_user_email"].label = "Email"

