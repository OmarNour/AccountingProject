from django.urls import include, path

from tax.views import TaxCreateView, TaxUpdateView
from . import views
from account_types import views as account_types_views
from chart_of_accounts import views as chart_of_accounts_views
from transactions import views as trans_views
from bill.views import BillView, Bills

app_name = 'organizations'

urlpatterns = [
    path('new/',views.CreateOrganization.as_view(), name='create'),
    path('',views.OrganizationList.as_view(), name='all'),
    path('<pk>', views.OrganizationDetailView.as_view(), name='detail'),
    path('edit/<pk>', views.OrganizationUpdateView.as_view(), name='edit'),
    path('delete/<pk>', views.OrganizationDeleteView.as_view(), name='delete'),


    # handling members
    path('add-member/<org_id>-<usr_id>', views.AddMember.as_view(), name='add-member'),
    path('delete-member/<org_id>-<usr_id>', views.DeleteMember.as_view(), name='delete-member'),

    # handling account types
    path('new-account-type/<org_id>',
        account_types_views.CreateAccountType.as_view(),
        name='create-account-type'),
    # path('delete-account-type/(?P<org_id>\w+)-(?P<acc_typ_code>\w+)$', account_types_views.DeleteAccountType.as_view(), name='delete-account-type'),
    path('edit-account-type/<org_id>-<acc_typ_code>-<pk>', account_types_views.AccountTypeUpdateView.as_view(), name='edit-account-type'),
    path('detail-account-type/<org_id>-<acc_typ_code>-<pk>', account_types_views.AccountTypeDetailView.as_view(), name='detail-account-type'),

    # handling chart of accounts
    path('new-account/<org_id>-<acc_typ_code_id>', chart_of_accounts_views.CreateChartOfAccountView.as_view(), name='create-account'),
    path('edit-account/<org_id>-<acc_typ_code_id>-<pk>', chart_of_accounts_views.UpdateChartOfAccountView.as_view(), name='edit-account'),

    # handling Currencies
    path('add-currency/<org_id>', views.CreateCurrenciesView.as_view(), name='add-currency'),
    path('edit-currency/<org_id>-<pk>', views.UpdateCurrenciesView.as_view(), name='edit-currency'),
    path('delete-currency/<org_id>-<pk>', views.DeleteCurrenciesView.as_view(), name='delete-currency'),

    # handling Exchange rates
    path('override-exchange-rate/<org_id>-<curr_id>-<pk>', views.OverrideOrgExchangeRateView.as_view(), name='override-exchange-rate'),

    # handling Transactions
    path('new-transaction/<org_id>', trans_views.CreateTransactionView.as_view(), name='new-transaction'),
    path('transactions/<org_id>', trans_views.TransactionsList.as_view(), name='transactions'),

    # Invite Users
    path('invite-user/<org_id>', views.InviteUserView.as_view(), name='invite-user'),

    # handling Taxes
    path('new-tax/<org_id>', TaxCreateView.as_view(), name='new-tax'),
    path('edit-tax/<org_id>-<pk>', TaxUpdateView.as_view(), name='edit-tax'),

    # handling Bills
    path('new-bill/<org_id>', BillView.as_view(), name='new-bill'),
    path('bills/<org_id>', Bills.as_view(), name='bills'),


]
