from django.db import models
from organizations.models import Organization
from django.contrib.auth import get_user_model
from vendor.models import Vendor

User = get_user_model()


class PurchaseOrder(models.Model):
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='PurchaseOrder_org_id')
    po_number = models.CharField(max_length=10, null=False, blank=False)

    delivery_date = models.DateField(null=True,blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=False, blank=False, related_name='PurchaseOrder_vendor')
    mark_as_billed = models.BooleanField(null=False, blank=False, default=False)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=User, related_name='PurchaseOrder_created_by')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='PurchaseOrder_modified_by')
    updated_date = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        unique_together = ('org_id', 'po_number')

    def __str__(self):
        return self.po_number


class PurchaseOrderDetail(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)

    def __str__(self):
        return self.purchase_order.po_number
