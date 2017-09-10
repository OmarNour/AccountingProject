from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import forms

from organizations.models import InvitedUsers


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('first_name','last_name', "username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"] = forms.EmailField(label='Email address',
                                                help_text='Required.',
                                                required=True)


class InvitationUserCreateForm(UserCreationForm,forms.ModelForm):
    class Meta:
        fields = ('first_name','last_name', "username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        # kwargs.pop('inv_id')
        # InvitedUsers
        self.inv_id_url = kwargs.pop('inv_id')
        try:
            invited_user = InvitedUsers.objects.get(id=self.inv_id_url)
        except InvitedUsers.DoesNotExist:
            invited_user = None

        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"

        self.fields["email"] = forms.EmailField(label='Email address',
                                                initial=invited_user.invited_user_email)

        self.fields['email'].widget.attrs['readonly'] = True

        self.fields["first_name"] = forms.CharField(initial=invited_user.invited_user_first_name)
        self.fields["last_name"] = forms.CharField(initial=invited_user.invited_user_last_name)
