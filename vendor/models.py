from django.db import models
from django.contrib.auth import get_user_model

from organizations.models import Organization

User = get_user_model()


class Vendor(models.Model):
    org_id = models.ForeignKey(Organization, related_name='Vendor_org_id')
    name = models.CharField(max_length=500, null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    site_url = models.URLField(null=True,blank=True)

    created_by = models.ForeignKey(User, default=User, related_name='Vendor_created_by')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.ForeignKey(User, null=True, blank=True, related_name='Vendor_modified_by')
    updated_date = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        unique_together = ('org_id', 'name')

    def __str__(self):
        return self.name
