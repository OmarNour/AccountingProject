from django.http import HttpResponseRedirect, HttpResponse
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

from AccountingApp.models import ExchangeRate, Currencies
from AccountingApp.views import get_exchange_rate
from organizations.forms import OrganizationUpdateForm, CreateOrganizationForm, CurrenciesForm, \
    OverrideOrgExchangeRateForm
from .models import Organization, OrganizationMember, OrgCurrencies, OrgExchangeRate


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


class OrganizationList(LoginRequiredMixin,generic.ListView):
    model = Organization

    def get_context_data(self, **kwargs):
        context = super(OrganizationList, self).get_context_data(**kwargs)
        context['UserOrganizations'] = Organization.objects.filter(owner=self.request.user).order_by('id')
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


class CreateCurrenciesView(LoginRequiredMixin, generic.CreateView):
    form_class = CurrenciesForm
    template_name = 'organizations/orgcurrencies_form.html'

    def get_success_url(self):
        return reverse_lazy('organizations:edit', kwargs={'pk': self.kwargs.get("org_id")})

    def get_form_kwargs(self):
        kwargs = super(CreateCurrenciesView, self).get_form_kwargs()
        kwargs.update({'org_id': self.kwargs.get("org_id")})
        return kwargs

    def form_valid(self, form):

        form.instance.created_by = self.request.user
        form.instance.Org_id = get_object_or_404(Organization, pk=self.kwargs.get("org_id"))

        form.save(commit=True)

        handle_exchange_rate(org_id=form.instance.Org_id,
                             from_currency_id=form.instance.currency_id,
                             new_base_currency=form.instance.base_currency)
        return super(CreateCurrenciesView, self).form_valid(form)


class UpdateCurrenciesView(LoginRequiredMixin, generic.UpdateView):
    form_class = CurrenciesForm
    template_name = 'organizations/orgcurrencies_form.html'

    def get_queryset(self):
        return OrgCurrencies.objects

    def get_success_url(self):
        return reverse_lazy('organizations:edit', kwargs={'pk': self.kwargs.get("org_id")})

    def get_form_kwargs(self):
        kwargs = super(UpdateCurrenciesView, self).get_form_kwargs()
        kwargs.update({'org_id': self.kwargs.get("org_id")})
        return kwargs

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        form.instance.modified_date = timezone.now()

        try:
            return super(UpdateCurrenciesView, self).form_valid(form)
        except IntegrityError:
            return HttpResponse("ERROR: Currency already exists!")


class DeleteCurrenciesView(LoginRequiredMixin, generic.DeleteView):
    model = OrgCurrencies

    def get_success_url(self):
        return reverse_lazy('organizations:edit', kwargs={'pk': self.kwargs.get("org_id")})


class OverrideOrgExchangeRateView(LoginRequiredMixin, generic.UpdateView):
    form_class = OverrideOrgExchangeRateForm
    template_name = 'organizations/org_exchange_rate_form.html'

    def get_queryset(self):
        return OrgExchangeRate.objects

    def get_success_url(self):
        return reverse_lazy('organizations:edit', kwargs={'pk': self.kwargs.get("org_id")})

    def get_form_kwargs(self):
        kwargs = super(OverrideOrgExchangeRateView, self).get_form_kwargs()
        kwargs.update({'org_id': self.kwargs.get("org_id")})
        kwargs.update({'curr_id': self.kwargs.get("curr_id")})
        kwargs.update({'pk': self.kwargs.get("pk")})

        return kwargs


# ############################# Standalone Functions ################################ #
def handle_exchange_rate(org_id, from_currency_id, new_base_currency):
    '''
    1- when new currency added-ok, updated or deleted
    2- when base currecny flag updated, then delete all and repopulate OrgExchangeRate
    '''
    swap = 0
    try:
        base_currency = OrgCurrencies.objects.filter(Org_id=org_id, base_currency=True).get()
    except OrgCurrencies.DoesNotExist:
        # print('DoesNotExist!!')
        base_currency_does_not_exist = True
    else:
        base_currency_does_not_exist = False

        if base_currency.currency_id != from_currency_id:
            base_currency_currencies = Currencies.objects.filter(currency_id=base_currency.currency_id)
            try:
                exchange_to_base_id = ExchangeRate.objects.filter().get(from_currency_id=from_currency_id,
                                                                        to_currency_id=base_currency_currencies)
            except ExchangeRate.DoesNotExist:
                swap = 1
                exchange_to_base_id = ExchangeRate.objects.filter().get(from_currency_id=base_currency_currencies,
                                                                        to_currency_id=from_currency_id)

            related_currency = OrgCurrencies.objects.filter(Org_id=org_id, currency_id=from_currency_id).get()
            try:
                if swap == 1:
                    swapped_current_rate = 1/exchange_to_base_id.rate
                else:
                    swapped_current_rate = exchange_to_base_id.rate
                OrgExchangeRate.objects.create(Org_id=org_id,
                                               ex_rate_id=exchange_to_base_id,
                                               related_OrgCurrencies=related_currency,
                                               from_currency_id=related_currency,
                                               to_currency_id=base_currency,
                                               swapped_current_rate=swapped_current_rate)
            except IntegrityError:
                pass

    if new_base_currency:
        # print('new base')
        # save the current override in a dictionary first
        from_currency_instance = Currencies.objects.filter(currency_id=from_currency_id).get()
        from_org_currency_instance = OrgCurrencies.objects.filter(Org_id=org_id, currency_id=from_currency_id).get()

        """
        override_dic = {}
        override_new_dic = {}
        if OrgExchangeRate.objects.filter(Org_id=org_id).count() > 0:

            for y in OrgExchangeRate.objects.filter(Org_id=org_id).all():
                override_dic[y.from_currency_id.currency_id.currency_id] = y.override_rate
                previous_base_currency_id = y.to_currency_id

            print('prev. base curr: {}'.format(previous_base_currency_id.currency_id))
            if not base_currency_does_not_exist:
                new_base_currency_id = base_currency.currency_id
            else:
                new_base_currency_id = from_org_currency_instance

            print('new base curr: {}'.format(new_base_currency_id.currency_id))
            print(override_dic)
        
        prev.base curr: EGP
        new base curr: SAR
        {'USD': Decimal('18.000000'), 'SAR': Decimal('5.000000')}
        
        for key, value in override_dic.items():
            # print('if {} == {}'.format(str(key),str(new_base_currency_id.currency_id)))

            if key == new_base_currency_id.currency_id.currency_id:
                override_new_dic[previous_base_currency_id.currency_id.currency_id] = 1/value if value != 0 else 0
            else:
                override_new_dic[key] = 0
        """
        OrgExchangeRate.objects.filter(Org_id=org_id).all().delete()
        # print('for loop')
        for x in OrgCurrencies.objects.filter(Org_id=org_id).exclude(currency_id=from_currency_instance).all():
            swap = 0

            related_currency = OrgCurrencies.objects.filter(Org_id=org_id, currency_id=x.currency_id).get()

            try:
                exchange_to_base_id = ExchangeRate.objects.filter().get(from_currency_id=x.currency_id,
                                                                        to_currency_id=from_currency_instance)
            except ExchangeRate.DoesNotExist:
                swap = 1
                exchange_to_base_id = ExchangeRate.objects.filter().get(from_currency_id=from_currency_instance,
                                                                        to_currency_id=x.currency_id)

            if swap == 1:
                swapped_current_rate = 1 / exchange_to_base_id.rate
            else:
                swapped_current_rate = exchange_to_base_id.rate

            OrgExchangeRate.objects.create(Org_id=org_id,
                                           ex_rate_id=exchange_to_base_id,
                                           related_OrgCurrencies=related_currency,
                                           from_currency_id=related_currency,
                                           to_currency_id=from_org_currency_instance,
                                           swapped_current_rate=swapped_current_rate,
                                           override_rate=0)



