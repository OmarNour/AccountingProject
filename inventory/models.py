from django.db import models
from organizations.models import Organization, Currencies
from django.contrib.auth import get_user_model
# from chart_of_accounts.models import ChartOfAccount

User = get_user_model()


class Inventory(models.Model):
    org_id = models.ForeignKey(Organization, related_name='Inventory_org_id')
    item_id = models.CharField(max_length=10, null=False, blank=False)
    qty = models.IntegerField(null=False,blank=False)
    ordered_qty = models.IntegerField(null=False, blank=False, default=0)
    sold_qty = models.IntegerField(null=False, blank=False, default=0)
    canceled_qty = models.IntegerField(null=False, blank=False, default=0)
    
    avg_cost = models.DecimalField(max_digits=30, decimal_places=6, null=False, blank=False)
    currency = models.ForeignKey(Currencies, null=False, related_name='Inventory_currency')
    # vendor
    # inventory_account = models.ForeignKey(ChartOfAccount, null=False, blank=False, related_name='Inventory_inventory_account')
    # cosg_account = models.ForeignKey(ChartOfAccount, null=False, blank=False, related_name='Inventory_cosg_account')

    created_by = models.ForeignKey(User, default=User, related_name='Inventory_created_by')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.ForeignKey(User, null=True, blank=True, related_name='Inventory_modified_by')
    updated_date = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        unique_together = ('org_id', 'item_id')

    def __str__(self):
        return self.item_id
