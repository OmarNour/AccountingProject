from django.conf.urls import url
from . import views
from AccountTypes import views as account_types_views
from chart_of_accounts import views as chart_of_accounts_views

app_name = 'organizations'

urlpatterns = [
    url(r'^(?i)new/$',views.CreateOrganization.as_view(), name='create'),
    url(r'^(?i)$',views.OrganizationList.as_view(), name='all'),
    url(r'^(?i)(?P<pk>\w+)$', views.OrganizationDetailView.as_view(), name='detail'),
    url(r'^(?i)edit/(?P<pk>\w+)$', views.OrganizationUpdateView.as_view(), name='edit'),
    url(r'^(?i)delete/(?P<pk>\w+)$', views.OrganizationDeleteView.as_view(), name='delete'),


    # handling members
    url(r'^(?i)add-member/(?P<org_id>\w+)-(?P<usr_id>\w+)$', views.AddMember.as_view(), name='add-member'),
    url(r'^(?i)delete-member/(?P<org_id>\w+)-(?P<usr_id>\w+)$', views.DeleteMember.as_view(), name='delete-member'),

    # handling account types
    url(r'^(?i)new-account-type/(?P<org_id>\w+)$',
        account_types_views.CreateAccountType.as_view(),
        name='create-account-type'),
    url(r'^(?i)delete-account-type/(?P<org_id>\w+)-(?P<acc_typ_code>\w+)$', account_types_views.DeleteAccountType.as_view(), name='delete-account-type'),
    url(r'^(?i)edit-account-type/(?P<org_id>\w+)-(?P<acc_typ_code>\w+)-(?P<pk>\w+)$', account_types_views.AccountTypeUpdateView.as_view(), name='edit-account-type'),

    # handling chart of accounts
    url(r'^(?i)new-account/(?P<org_id>\w+)-(?P<acc_typ_code_id>\w+)$', chart_of_accounts_views.CreateChartOfAccountView.as_view(), name='create-account'),
    url(r'^(?i)edit-account/(?P<org_id>\w+)-(?P<acc_typ_code_id>\w+)-(?P<pk>\w+)$', chart_of_accounts_views.UpdateChartOfAccountView.as_view(), name='edit-account'),

]