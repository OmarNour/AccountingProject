from django.contrib import admin
from organizations.models import Organization,OrganizationMember,OrgCurrencies,OrgExchangeRate
# Register your models here.

admin.site.register(Organization)
admin.site.register(OrganizationMember)
admin.site.register(OrgCurrencies)
admin.site.register(OrgExchangeRate)
