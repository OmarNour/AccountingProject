from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import models

from AccountingApp.models import Sign
from organizations.models import Organization


User = get_user_model()


class AccountTypes(models.Model):
    # Assets = Liabilities + Equity/Capital + Income/Revenue - Expenses

    # print(md_user)
    org_id = models.ForeignKey(Organization,
                               # default=Organization.objects.filter().get(),
                               related_name='accountType_org_id')
    code = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=500)
    main_code = models.ForeignKey('self', null=True, blank=True, related_query_name='orgID')

    dr_sign = models.ForeignKey(Sign, null=False, blank=False, related_name='account_type_dr_sign')
    cr_sign = models.ForeignKey(Sign, null=False, blank=False, related_name='account_type_cr_sign')

    created_by = models.ForeignKey(User, default=User, related_name='accountType_created_by')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.ForeignKey(User, null=True, blank=True, related_name='accountType_modified_by')
    updated_date = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        unique_together = (('org_id', 'code'),('org_id', 'name'))

    def get_absolute_url(self):
        return reverse("accountTypes:detail", kwargs={'pk': self.pk})

    def __str__(self):
        return '{}'.format(self.name)
