from django.urls import include, path
from AccountingApp import views

app_name = 'AccountingApp'
urlpatterns = [
    # url('$', views.index, name='index'),
    # path('', views.home, name='home'),

    path('settings/', views.settings, name='settings'),
    path('accounts-types/', views.account_types, name='accounts_types'),
    path('chart-of-accounts/', views.chart_of_accounts, name='chart_of_accounts'),
    path('account/<code>/', views.get_account_by_code, name='get_account_by_code'),
    path('edit-account/<code>/', views.edit_account_by_code, name='edit_account_by_code'),
    path('new-account/', views.chart_of_accounts_new, name='chart_of_accounts_new'),
    path('new-transaction/', views.add_transaction, name='add_transaction'),
    path('all-transactions/', views.all_transactions, name='all_transactions'),
    path('transaction/<transaction_id>)/', views.get_transaction_by_id, name='get_transaction_by_id'),
    path('edit-transaction/<transaction_id>/', views.edit_transaction_by_id, name='edit_transaction_by_id'),
    # url('export/(.*)', views.export_data, name="export"),
    path('export/<atype>/', views.export_data, name="export"),  # working fine
    path('import/', views.import_data, name="import"),
    path('import_sheet/', views.import_sheet, name="import_sheet"),  # working fine
    path('handson_view/', views.handson_table, name="handson_view"),

    #url('user_login/', views.user_login, name='user_login'),
]


