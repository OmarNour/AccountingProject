from django.http import HttpResponseRedirect
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.models import User

from organizations.forms import OrganizationUpdateForm, CreateOrganizationForm
from .models import Organization, OrganizationMember


class CreateOrganization(LoginRequiredMixin, generic.CreateView):
    model = Organization
    form_class = CreateOrganizationForm
    template_name = 'organizations/organization_form.html'
    # permission_required = 'organizations.CreateOrganization'
    # fields = ('id', 'name', 'email', 'main_org')
    # success_url = reverse_lazy('organizations:all')

    def get_success_url(self):
        return reverse_lazy('organizations:all')

    def form_valid(self, form):

        form.instance.created_by = self.request.user
        form.instance.owner = self.request.user

        form.save(commit=True)
        organization = get_object_or_404(Organization, pk=form.instance.id)
        OrganizationMember.objects.create(user=self.request.user, organization_id=organization)

        return super(CreateOrganization, self).form_valid(form)
    """
    def get_form_kwargs(self):
        kwargs = super(CreateOrganization, self).get_form_kwargs()
        # kwargs.update({'user': self.request.user})
        kwargs.update({'owner_org_id': self.kwargs.get("pk")})
        kwargs.update({'exclude_org_id': self.kwargs.get("pk")})
        return kwargs
    """


class OrganizationList(LoginRequiredMixin,generic.ListView):
    model = Organization

    def get_context_data(self, **kwargs):
        context = super(OrganizationList, self).get_context_data(**kwargs)
        context['UserOrganizations'] = Organization.objects.filter(owner=self.request.user).order_by('id')  # whatever you would like
        return context


class OrganizationDetailView(LoginRequiredMixin,generic.DetailView):
    model = Organization


class OrganizationUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Organization
    form_class = OrganizationUpdateForm
    template_name = 'organizations/organization_form.html'

    # fields = ['id','name', 'email', 'main_org']
    # success_url = reverse_lazy('organizations:all')

    def get_queryset(self):
        return Organization.objects.filter(id=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy('organizations:all')

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.modified_date = timezone.now()
        return super(OrganizationUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(OrganizationUpdateView, self).get_form_kwargs()
        # kwargs.update({'user': self.request.user})
        kwargs.update({'owner_org_id': self.kwargs.get("pk")})
        kwargs.update({'exclude_org_id': self.kwargs.get("pk")})
        return kwargs


class OrganizationDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Organization
    success_url = reverse_lazy('organizations:all')


class AddMember(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        return reverse("organizations:edit", kwargs={"pk": self.kwargs.get("org_id")})

    def get(self, request, *args, **kwargs):
        """""
        member = OrganizationMember.objects.filter(organization_id=self.kwargs.get("org_id"),
                                                   user=self.kwargs.get("usr_id")).get()
        """""
        # organization = get_object_or_404(Organization, org_id=self.kwargs.get("org_id"))
        user = User.objects.get(id=self.kwargs.get("usr_id"))
        organization = Organization.objects.get(id=self.kwargs.get("org_id"))

        try:

            OrganizationMember.objects.create(user=user, organization_id=organization)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(organization.name)))

        else:
            messages.success(self.request,"You are now a member of the {} organization.".format(organization.name))

        return super().get(request, *args, **kwargs)


class DeleteMember(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("organizations:edit", kwargs={"pk": self.kwargs.get("org_id")})

    def get(self, request, *args, **kwargs):

        try:

            member = OrganizationMember.objects.filter(organization_id=self.kwargs.get("org_id"),
                                                       user=self.kwargs.get("usr_id")).get()

        except OrganizationMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this organization because you aren't in it."
            )
        else:
            member.delete()
            messages.success(
                self.request,
                "Successfully left the organization."
            )
        return super().get(request, *args, **kwargs)
