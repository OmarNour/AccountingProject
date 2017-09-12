from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import formset_factory
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from bill.forms import BillForm, BillDetailsFormSet
from bill.models import Bill, BillDetails
from chart_of_accounts.models import ChartOfAccount
from inventory.models import Inventory
from organizations.models import Organization
from transactions.views import create_new_transaction


class BillView(LoginRequiredMixin, generic.CreateView):
    form_class = BillForm
    template_name = 'bill/bill_form.html'

    def get_form_kwargs(self):
        kwargs = super(BillView, self).get_form_kwargs()
        kwargs.update({'org_id': self.kwargs.get("org_id")})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(BillView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['bill_details'] = BillDetailsFormSet(self.request.POST,
                                                      form_kwargs={'org_id': self.kwargs.get("org_id")})
        else:
            context['bill_details'] = BillDetailsFormSet(form_kwargs={'org_id': self.kwargs.get("org_id")})
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        bill_details = context['bill_details']

        with transaction.atomic():
            organization = Organization.objects.filter(id=self.kwargs.get("org_id")).get()
            form.instance.org_id = organization
            form.instance.created_by = self.request.user
            form.instance.created_date = timezone.datetime.now()

            # print(self.request.POST)
            # bill_details.instance.bill = self.object
            if bill_details.is_valid():
                self.object = form.save(commit=True)
                # print('pass is valid')
                bill_details.instance.bill = self.object
                bill_details.instance.created_by = self.request.user
                bill_details.instance.created_date = timezone.datetime.now()
                for i in range(0, int(self.request.POST['BillDetails_bill-TOTAL_FORMS'])):
                    if self.request.POST['BillDetails_bill-'+str(i)+'-description']:
                        if self.request.POST['BillDetails_bill-'+str(i)+'-item']:
                            item = Inventory.objects.get(id=int(self.request.POST['BillDetails_bill-'+str(i)+'-item']))
                        else:
                            item = None

                        dr_account = ChartOfAccount.objects.get(id=int(self.request.POST['BillDetails_bill-'+str(i)+'-dr_account']))

                        cr_account = ChartOfAccount.objects.get(id=int(self.request.POST[
                                                                    'BillDetails_bill-' + str(i) + '-cr_account']))
                        qty = int(self.request.POST['BillDetails_bill-' + str(i) + '-qty'])
                        unit_price = Decimal(self.request.POST['BillDetails_bill-' + str(i) + '-unit_price'])
                        amount = qty * unit_price
                        bill_record = BillDetails.objects.create(bill=self.object,
                                                                 item=item,
                                                                 description=self.request.POST['BillDetails_bill-'+str(i)+'-description'],
                                                                 qty=qty,
                                                                 unit_price=unit_price,
                                                                 amount=amount,
                                                                 dr_account=dr_account,
                                                                 cr_account=cr_account,
                                                                 created_by=bill_details.instance.created_by,
                                                                 created_date=bill_details.instance.created_date,
                                                   )
                        # print(self.object.org_id)
                        create_new_transaction(org_id=self.object.org_id,
                                               source_key='BILL',
                                               source_record=bill_record)

                # bill_details.save()
            else:
                return super(BillView, self).form_invalid(form)
        return super(BillView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('organizations:detail', kwargs={'pk': self.kwargs.get("org_id")})


class Bills(LoginRequiredMixin, generic.ListView):
    form_class = BillForm
    template_name = 'bill/bills.html'

    def get_context_data(self, **kwargs):
        context = super(Bills, self).get_context_data(**kwargs)
        context['org_id'] = self.kwargs.get("org_id")
        context['OrgBills'] = Bill.objects.filter(org_id=self.kwargs.get("org_id")).order_by('-id')
        return context

