from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin
)

from django.urls import reverse, reverse_lazy
# from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth.models import User

from .models import AccountType, Organization
# from braces.views import SelectRelatedMixin
# from users_accounts.middleware import filter_ip_middleware
# md_user = filter_ip_middleware.FilterIPMiddleware

from .forms import CreateAccountTypeForm,UpdateAccountTypeForm


class CreateAccountType(LoginRequiredMixin, generic.CreateView):
    form_class = CreateAccountTypeForm
    template_name = "AccountTypes/accounttypes_form.html"

    def get_form_kwargs(self):
        kwargs = super(CreateAccountType, self).get_form_kwargs()
        kwargs.update({'org_id': self.kwargs.get("org_id")})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('organizations:detail', kwargs={'pk': self.kwargs.get("org_id")})

    def form_valid(self, form):

        form.instance.created_by = self.request.user
        organization = get_object_or_404(Organization, pk=self.kwargs.get("org_id"))
        form.instance.org_id = organization

        return super(CreateAccountType, self).form_valid(form)


# class AccountTypesListView(LoginRequiredMixin,SelectRelatedMixin, generic.ListView):
#     model = AccountType
    # select_related = 'org_id'


class AccountTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = AccountType
    template_name = "AccountTypes/accounttype_detail.html"

    # def get_queryset(self):
    #     return AccountType.objects.filter(org_id_id=self.kwargs.get("org_id"))# implicity filters with pk givin from url


class AccountTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = UpdateAccountTypeForm
    # fields = ('id', 'code', 'name', 'main_code')
    template_name = "AccountTypes/accounttypes_form.html"
    # org_id = None
    # acc_typ_code = None

    def get_queryset(self):
        return AccountType.objects.filter(org_id_id=self.kwargs.get("org_id"))# implicity filters with pk givin from url

    def get_form_kwargs(self):
        kwargs = super(AccountTypeUpdateView, self).get_form_kwargs()
        kwargs.update({'org_id': self.kwargs.get("org_id")})
        kwargs.update({'acc_typ_code': self.kwargs.get("acc_typ_code")})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('organizations:detail', kwargs={'pk': self.kwargs.get("org_id")})

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.modified_date = timezone.datetime.now()
        return super(AccountTypeUpdateView, self).form_valid(form)


class DeleteAccountType(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("organizations:detail", kwargs={"pk": self.kwargs.get("org_id")})

    def get(self, request, *args, **kwargs):

        try:

            account_type = AccountType.objects.filter(org_id=self.kwargs.get("org_id"),
                                                      code=self.kwargs.get("acc_typ_code")).get()

        except AccountType.DoesNotExist:
            messages.warning(
                self.request,
                "Account type does not exists"
            )
        else:
            account_type.delete()
            messages.success(
                self.request,
                "Successfully deleted."
            )
        return super().get(request, *args, **kwargs)




