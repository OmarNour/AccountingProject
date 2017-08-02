from django.conf.urls import url
from AccountingApp import views

app_name = 'AccountingApp'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^(?i)settings/', views.settings, name='settings'),
    url(r'^(?i)register/', views.register, name='register'),
    url(r'^(?i)user_login/$',views.user_login,name='user_login'),
    url(r'^(?i)accounts-types/', views.account_types, name='accounts_types'),
    url(r'^(?i)chart-of-accounts/', views.chart_of_accounts, name='chart_of_accounts'),
    url(r'^(?i)account/(?P<code>\w+)/$', views.get_account_by_code, name='get_account_by_code'),
    url(r'^(?i)edit-account/(?P<code>\w+)/$', views.edit_account_by_code, name='edit_account_by_code'),
    url(r'^(?i)new-account/', views.chart_of_accounts_new, name='chart_of_accounts_new'),
    url(r'^(?i)new-transaction/', views.add_transaction, name='add_transaction'),
    url(r'^(?i)all-transactions/', views.all_transactions, name='all_transactions'),
    url(r'^(?i)transaction/(?P<transaction_id>\w+)/$', views.get_transaction_by_id, name='get_transaction_by_id'),
    url(r'^(?i)edit-transaction/(?P<transaction_id>\w+)/$', views.edit_transaction_by_id, name='edit_transaction_by_id'),

    #url(r'^(?i)user_login/', views.user_login, name='user_login'),
]


