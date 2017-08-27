from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.core.urlresolvers import reverse_lazy
from django.views import generic


# Create your views here.
from AccountingApp.models import TransactionSources, AccountTypesDrCr
from AccountTypes.models import AccountTypes
from chart_of_accounts.models import ChartOfAccounts
from organizations.models import OrgExchangeRate, Organization
from transactions.forms import TransactionForm
from transactions.models import Transaction


class CreateTransactionView(LoginRequiredMixin, generic.CreateView):
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'

    def get_success_url(self):
        return reverse_lazy('organizations:edit', kwargs={'pk': self.kwargs.get("org_id")})
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


# ############################### standalone functions ############################ #
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
    return ChartOfAccounts.objects.get(org_id=org_id,
                                       type_code_id=account_type,
                                       code=account_code)


def validate_transaction(org_id,
                         dr_type_code,
                         dr_account_code,
                         cr_type_code,
                         cr_account_code
                         ):
    if dr_account_code != cr_account_code:
        dr_type_code = get_chart_of_accounts_type_code(org_id, dr_type_code, dr_account_code)
        cr_type_code = get_chart_of_accounts_type_code(org_id, cr_type_code, cr_account_code)
        # print('validate_transaction')
        # print(dr_type_code.type_code.code)
        dr_sign = AccountTypes.objects.get(org_id=org_id, code=dr_type_code.type_code.code)
        cr_sign = AccountTypes.objects.get(org_id=org_id, code=cr_type_code.type_code.code)
        # print(dr_sign.dr_sign)
        if dr_sign.dr_sign == cr_sign.cr_sign:
            return False
        else:
            return True
    else:
        return False

