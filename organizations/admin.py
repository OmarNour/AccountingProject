from django.contrib import admin
from organizations.models import Organization,OrganizationMember
# Register your models here.

admin.site.register(Organization)
admin.site.register(OrganizationMember)
