from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from chart_of_accounts.models import ChartOfAccounts
from organizations.models import Organization
from AccountTypes.models import AccountTypes
from .forms import CreateChartOfAccountForm, UpdateChartOfAccountForm


class CreateChartOfAccountView(LoginRequiredMixin, generic.CreateView):
    form_class = CreateChartOfAccountForm
    template_name = "chart_of_accounts/chart_of_accounts_form.html"

    def get_context_data(self, **kwargs):
        context = super(CreateChartOfAccountView, self).get_context_data(**kwargs)
        context['account_type'] = AccountTypes.objects.filter(id=self.kwargs.get("acc_typ_code_id")).get()
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateChartOfAccountView, self).get_form_kwargs()
        # kwargs.update({'org_id': self.kwargs.get("org_id")})
        kwargs.update({'acc_typ_code_id': self.kwargs.get("acc_typ_code_id")})
        return kwargs

    def get_success_url(self):
        acc_typ_code = AccountTypes.objects.filter(id=self.kwargs.get("acc_typ_code_id")).get()
        return reverse_lazy('organizations:edit-account-type', kwargs={'org_id': self.kwargs.get("org_id"),
                                                                       'acc_typ_code': acc_typ_code.code,
                                                                       'pk': self.kwargs.get("acc_typ_code_id")})

    def form_valid(self, form):
        account_type = get_object_or_404(AccountTypes, id=self.kwargs.get("acc_typ_code_id"))
        form.instance.type_code = account_type
        form.instance.created_by = self.request.user
        organization = get_object_or_404(Organization, pk=self.kwargs.get("org_id"))
        form.instance.org_id = organization

        return super(CreateChartOfAccountView, self).form_valid(form)


class UpdateChartOfAccountView(LoginRequiredMixin, generic.UpdateView):
    form_class = UpdateChartOfAccountForm
    template_name = "chart_of_accounts/chart_of_accounts_form.html"

    def get_queryset(self):
        return ChartOfAccounts.objects

    def get_context_data(self, **kwargs):
        context = super(UpdateChartOfAccountView, self).get_context_data(**kwargs)
        context['account_type'] = AccountTypes.objects.filter(id=self.kwargs.get("acc_typ_code_id")).get()
        return context

    def get_form_kwargs(self):
        kwargs = super(UpdateChartOfAccountView, self).get_form_kwargs()
        kwargs.update({'account_id': self.kwargs.get("pk")})
        kwargs.update({'acc_typ_code_id': self.kwargs.get("acc_typ_code_id")})
        return kwargs

    def get_success_url(self):
        acc_typ_code = AccountTypes.objects.filter(id=self.kwargs.get("acc_typ_code_id")).get()
        return reverse_lazy('organizations:edit-account-type', kwargs={'org_id': self.kwargs.get("org_id"),
                                                                       'acc_typ_code': acc_typ_code.code,
                                                                       'pk': self.kwargs.get("acc_typ_code_id")})

    def form_valid(self, form):
        account_type = get_object_or_404(AccountTypes, id=self.kwargs.get("acc_typ_code_id"))
        form.instance.type_code = account_type
        form.instance.created_by = self.request.user
        organization = get_object_or_404(Organization, pk=self.kwargs.get("org_id"))
        form.instance.org_id = organization

        return super(UpdateChartOfAccountView, self).form_valid(form)
