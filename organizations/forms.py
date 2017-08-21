from .models import Organization, OrganizationMember
from django.contrib.auth.forms import forms


class CreateOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'email', 'main_org')

    """
    def __init__(self, *args, **kwargs):
        # self.fields["username"].label = "Display name"
        # self.fields["email"].label = "Email address"

        # org_owner = Organization.objects.filter(id=kwargs.pop('org_id')).get().owner
        org_owner = Organization.objects.filter(id=kwargs.pop('owner_org_id')).get().owner

        related_organizations = Organization.objects.\
                                filter(owner=org_owner).\
                                exclude(id=kwargs.pop('exclude_org_id'))

        super().__init__(*args, **kwargs)
        self.fields['main_org'] = forms.ModelChoiceField(queryset=related_organizations, required=False)
    """


class OrganizationUpdateForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('id','name', 'email', 'main_org')

    def __init__(self, *args, **kwargs):

        # self.fields["username"].label = "Display name"
        # self.fields["email"].label = "Email address"

        # org_owner = Organization.objects.filter(id=kwargs.pop('org_id')).get().owner
        org_owner = Organization.objects.filter(id=kwargs.pop('owner_org_id')).get().owner

        related_organizations = Organization.objects.\
                                filter(owner=org_owner).\
                                exclude(id=kwargs.pop('exclude_org_id'))

        super().__init__(*args, **kwargs)
        self.fields['main_org'] = forms.ModelChoiceField(queryset=related_organizations, required=False)

