from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from bill.forms import BillForm, BillDetailsFormSet
from bill.models import Bill
from organizations.models import Organization


class BillView(LoginRequiredMixin, generic.CreateView):
    form_class = BillForm
    template_name = 'bill/bill_form.html'

    def get_form_kwargs(self):
        kwargs = super(BillView, self).get_form_kwargs()
        kwargs.update({'org_id': self.kwargs.get("org_id")})
        return kwargs

    def get_context_data(self, **kwargs):
        data = super(BillView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['bill_details'] = BillDetailsFormSet(self.request.POST)
        else:
            data['bill_details'] = BillDetailsFormSet(form_kwargs={'org_id': self.kwargs.get("org_id")})
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        bill_details = context['bill_details']
        with transaction.atomic():
            organization = Organization.objects.filter(id=self.kwargs.get("org_id")).get()
            form.instance.org_id = organization
            form.instance.created_by = self.request.user
            form.instance.created_date = timezone.datetime.now()
            self.object = form.save()
        if bill_details.is_valid():
            bill_details.instance = self.object
            bill_details.save()

        return super(BillView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('organizations:bills', kwargs={'org_id': self.kwargs.get("org_id")})


class Bills(LoginRequiredMixin, generic.ListView):
    form_class = BillForm
    template_name = 'bill/bills.html'

    def get_context_data(self, **kwargs):
        context = super(Bills, self).get_context_data(**kwargs)
        context['org_id'] = self.kwargs.get("org_id")
        context['OrgBills'] = Bill.objects.filter(org_id=self.kwargs.get("org_id")).order_by('-id')
        return context

