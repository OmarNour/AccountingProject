import datetime

from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.core.urlresolvers import reverse_lazy
from django.views import generic
import calendar

# Create your views here.
from AccountingApp.models import TransactionSources
from account_types.models import AccountType
from bill.models import BillDetails
from organizations.models import OrgExchangeRate, OrgCurrencies
from .forms import TransactionForm
from .models import Transaction, Organization, ChartOfAccount


class CreateTransactionView(LoginRequiredMixin, generic.CreateView):
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'

    def get_success_url(self):
        return reverse_lazy('organizations:detail', kwargs={'pk': self.kwargs.get("org_id")})
        # return reverse_lazy('organizations:transactions', kwargs={'org_id': self.kwargs.get("org_id")})

    def get_context_data(self, **kwargs):
        context = super(CreateTransactionView, self).get_context_data(**kwargs)
        context['organization'] = Organization.objects.filter(id=self.kwargs.get("org_id")).get()
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateTransactionView, self).get_form_kwargs()
        kwargs.update({'org_id': self.kwargs.get("org_id")})
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # form.save(commit=True)
        organization = Organization.objects.filter(id=self.kwargs.get("org_id")).get()
        transaction_source = TransactionSources.objects.filter(source_key='MAN').get()

        form.instance.org_id = organization
        form.instance.transaction_source = transaction_source
        form.instance.transaction_id = get_new_transaction_id(organization.id)
        form.instance.exchange_rate = get_exchange_rate(org_id=organization.id,
                                                        from_currency_id=form.instance.currency_id,
                                                        to_currency_id=form.instance.base_currency_id)
        form.instance.base_eqv_amount = form.instance.amount*form.instance.exchange_rate
        return super(CreateTransactionView, self).form_valid(form)


class TransactionsList(LoginRequiredMixin, generic.ListView):
    model = Transaction

    def get_context_data(self, **kwargs):
        context = super(TransactionsList, self).get_context_data(**kwargs)
        context['org_id'] = self.kwargs.get("org_id")
        context['OrgTransactions'] = Transaction.objects.filter(org_id=self.kwargs.get("org_id")).order_by('-id')
        return context

                # ################################################################################# #
                # ############################### standalone functions ############################ #
                # ################################################################################# #


def create_new_transaction(org_id, source_key, source_record, validate_transaction=False):
    create_trans = False
    create_tax_trans = False
    source = TransactionSources.objects.get(source_key=source_key)
    if source_key == 'BILL':
        # source_record = BillDetails.objects.get(id=source_record)
        transaction_date = source_record.bill.bill_date
        value_date = source_record.bill.due_date
        amount = source_record.amount
        dr_account_code = source_record.dr_account
        cr_account_code = source_record.cr_account
        currency_id = source_record.bill.currency
        base_currency_id = get_base_currency(org_id)
        exchange_rate = get_exchange_rate(org_id, currency_id, base_currency_id)
        base_eqv_amount = amount * exchange_rate
        narrative = source_record.description
        transaction_source = source
        reference_number = source_record.id
        created_by = source_record.created_by
        created_date = source_record.created_date

        if source_record.bill.amounts_are_id != 3:
            num_days = calendar.monthrange(transaction_date.year, transaction_date.month)[1]
            tax_value_date = datetime.date(transaction_date.year, transaction_date.month, num_days)
            tax_amount = source_record.tax_amount
            tax_cr_account_code = source_record.tax.tax_account
            tax_base_eqv_amount = tax_amount * exchange_rate

            create_tax_trans = True

        create_trans = True
    elif source_key == 'INV':
        pass
    elif source_key == 'ECLM':
        pass
    else:
        create_trans = False

    if create_trans:
        new_transaction = Transaction.objects.create(org_id=org_id,
                                                     transaction_id=get_new_transaction_id(org_id),
                                                     transaction_date=transaction_date,
                                                     value_date=value_date,
                                                     amount=amount,
                                                     dr_account_code=dr_account_code,
                                                     cr_account_code=cr_account_code,
                                                     currency_id=currency_id,
                                                     base_currency_id=base_currency_id,
                                                     exchange_rate=exchange_rate,
                                                     base_eqv_amount=base_eqv_amount,
                                                     narrative=narrative,
                                                     void=False,
                                                     transaction_source=transaction_source,
                                                     reference_number=reference_number,
                                                     created_by=created_by,
                                                     created_date=created_date
                                                    )
        if create_tax_trans:
            tax_transaction = Transaction.objects.create(org_id=org_id,
                                                         transaction_id=get_new_transaction_id(org_id),
                                                         transaction_date=transaction_date,
                                                         value_date=tax_value_date,
                                                         amount=tax_amount,
                                                         dr_account_code=dr_account_code,
                                                         cr_account_code=tax_cr_account_code,
                                                         currency_id=currency_id,
                                                         base_currency_id=base_currency_id,
                                                         exchange_rate=exchange_rate,
                                                         base_eqv_amount=tax_base_eqv_amount,
                                                         narrative=narrative,
                                                         void=False,
                                                         transaction_source=transaction_source,
                                                         reference_number=reference_number,
                                                         created_by=created_by,
                                                         created_date=created_date
                                                         )
        if source_key == 'BILL':
            BillDetails.objects.filter(id=source_record.id).update(trnx_number=new_transaction)
        elif source_key == 'INV':
            pass
        elif source_key == 'ECLM':
            pass


def get_base_currency(org_id):
    # print(org_id.id)
    return OrgCurrencies.objects.get(Org_id=org_id,
                                     base_currency=True)


def get_new_transaction_id(org_id):
    last_trnx_id = Transaction.objects.filter(org_id=org_id).order_by('id').last()
    if not last_trnx_id:
        return 1
    new_trnx_id = last_trnx_id.transaction_id + 1
    return new_trnx_id


def get_exchange_rate(org_id, from_currency_id, to_currency_id):
    swap = 0
    if from_currency_id != to_currency_id:
        try:
            exchange_rate = OrgExchangeRate.objects.get(Org_id=org_id,
                                                        from_currency_id=from_currency_id,
                                                        to_currency_id=to_currency_id)
        except OrgExchangeRate.DoesNotExist:
            try:
                exchange_rate = OrgExchangeRate.objects.get(from_currency_id=to_currency_id, to_currency_id=from_currency_id)
                swap = 1
            except OrgExchangeRate.DoesNotExist:
                exchange_rate = None

        if exchange_rate is not None:
            rate = exchange_rate.override_rate if exchange_rate.override_rate > 0 else exchange_rate.ex_rate_id.rate
            if swap == 0:
                return rate
            else:
                return 1/rate
        else:
            return 0

    else:
        return 1


def get_chart_of_accounts_type_code(org_id, account_type, account_code):
    # print('get_chart_of_accounts_type_code')
    # print(org_id)
    # print(account_type)
    # print(account_code)
    return ChartOfAccount.objects.get(org_id=org_id,
                                      type_code_id=account_type,
                                      code=account_code)


def valid_transaction(org_id,
                      dr_type_code,
                      dr_account_code,
                      cr_type_code,
                      cr_account_code
                      ):
    if dr_account_code != cr_account_code:
        dr_type_code = get_chart_of_accounts_type_code(org_id, dr_type_code, dr_account_code)
        cr_type_code = get_chart_of_accounts_type_code(org_id, cr_type_code, cr_account_code)
        # print('valid_transaction')
        # print(dr_type_code.type_code.code)
        dr_sign = AccountType.objects.get(org_id=org_id, code=dr_type_code.type_code.code)
        cr_sign = AccountType.objects.get(org_id=org_id, code=cr_type_code.type_code.code)
        # print(dr_sign.dr_sign)
        if dr_sign.dr_sign == cr_sign.cr_sign:
            return False
        else:
            return True
    else:
        return False

