from django.contrib.auth import login, logout
# from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from django.contrib.auth.models import User
from organizations.models import OrganizationMember, InvitedUsers, Organization
from . import forms


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


class InvitationSignUp(CreateView):
    form_class = forms.InvitationUserCreateForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

    def get_form_kwargs(self):
        kwargs = super(InvitationSignUp, self).get_form_kwargs()
        kwargs.update({'inv_id': self.kwargs.get("inv_id")})
        return kwargs

    def form_valid(self, form):
        form.save(commit=True)
        if form.is_valid():
            # invited_user = InvitedUsers.objects.get(id=self.kwargs.get("inv_id"))
            user = User.objects.get(email=form.instance.email)
            organization = Organization.objects.get(id=self.kwargs.get("org_id"))
            invitation = InvitedUsers.objects.get(id=self.kwargs.get("inv_id"))
            OrganizationMember.objects.create(user=user,
                                              organization_id=organization,
                                              invitation_id=invitation,
                                              active=True)
            InvitedUsers.objects.filter(pk=self.kwargs.get("inv_id")).update(invited_user=user,
                                                                             invitation_accepted_date= timezone.now())
        return super(InvitationSignUp, self).form_valid(form)
