from django.db import models
from organizations.models import Organization
from django.contrib.auth import get_user_model
from chart_of_accounts.models import ChartOfAccount
User = get_user_model()


class Tax(models.Model):
    org_id = models.ForeignKey(Organization, related_name='Tax_org_id')
    tax_id = models.CharField(max_length=10, null=False, blank=False)
    tax_desc = models.CharField(null=False, blank=False, max_length=100)
    tax_account = models.ForeignKey(ChartOfAccount, null=False, blank=False, related_name='Tax_tax_account')
    total_tax_pct = models.DecimalField(null=False,blank=False, default=0, max_digits=10, decimal_places=4)

    created_by = models.ForeignKey(User, default=User, related_name='Tax_created_by')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.ForeignKey(User, null=True, blank=True, related_name='Tax_modified_by')
    updated_date = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        unique_together = ('org_id', 'tax_id')

    def __str__(self):
        return '{} {}%'.format(self.tax_desc,self.total_tax_pct)




class TaxComponents(models.Model):
    id = models.AutoField(null=False, blank=False, primary_key=True)
    tax_id = models.ForeignKey(Tax, null=False, blank=False, related_name='TaxComponents_tax')

    component_desc = models.CharField(null=False, blank=False, max_length=100)
    percentage = models.DecimalField(null=False,blank=False,default=0, max_digits=10, decimal_places=4)
    compound = models.BooleanField(null=False, blank=False, default=False)

    created_by = models.ForeignKey(User, default=User, related_name='TaxComponents_created_by')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.ForeignKey(User, null=True, blank=True, related_name='TaxComponents_modified_by')
    updated_date = models.DateTimeField(null=True, blank=True, editable=True)

    class Meta:
        unique_together = ('tax_id', 'id')

    def __str__(self):
        return self.percentage
