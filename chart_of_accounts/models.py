from django.db import models

# Create your models here.
from django.urls import reverse

from AccountTypes.models import AccountTypes
from organizations.models import Organization
from django.contrib.auth import get_user_model

User = get_user_model()


class ChartOfAccounts(models.Model):
    org_id = models.ForeignKey(Organization, related_name='ChartOfAccounts_org_id')
    code = models.IntegerField(null=False,blank=False)
    name = models.CharField(null=False,blank=False,max_length=500)
    type_code = models.ForeignKey(AccountTypes, null=False, blank=False, related_name='ChartOfAccounts_type_code')
    main_code = models.ForeignKey('self', null=True, blank=True, related_name='ChartOfAccounts_main_code')

    created_by = models.ForeignKey(User, default=User, related_name='ChartOfAccounts_created_by')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.ForeignKey(User, null=True, blank=True, related_name='ChartOfAccounts_modified_by')
    updated_date = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        unique_together = (('org_id', 'type_code', 'code'),('org_id','type_code', 'name'))

    def get_absolute_url(self):
        return reverse("chart_of_accounts:detail", kwargs={'pk': self.pk})

    def __str__(self):
        return '{} - {}'.format(self.name, self.type_code)