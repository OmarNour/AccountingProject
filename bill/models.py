from django.db import models

from AccountingApp.models import LOV
from organizations.models import Organization, OrgCurrencies
from django.contrib.auth import get_user_model
from chart_of_accounts.models import ChartOfAccount
from inventory.models import Inventory
from purchase_order.models import PurchaseOrder
from tax.models import Tax
from transactions.models import Transaction
from vendor.models import Vendor

User = get_user_model()


class Bill(models.Model):
    org_id = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='Bill_org_id')
    bill_no = models.CharField(max_length=10, null=False, blank=False)
    po_number = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True, blank=True, related_name='Bill_po_number')
    currency = models.ForeignKey(OrgCurrencies, on_delete=models.CASCADE, null=False, blank=False, related_name='Bill_currency')
    bill_date = models.DateField(null=False,blank=False)
    amounts_are = models.ForeignKey(LOV, on_delete=models.CASCADE, null=False, blank=False, related_name='Bill_amounts_are_LOV')
    total_amount = models.DecimalField(max_digits=30, decimal_places=6, null=False, blank=False)
    total_tax_amount = models.DecimalField(max_digits=30, decimal_places=6, null=False, blank=False)
    due_date = models.DateField(null=False, blank=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=False, blank=False, related_name='bill_vendor')

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=User, related_name='Bill_created_by')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='Bill_modified_by')
    updated_date = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        unique_together = ('org_id', 'bill_no')

    def __str__(self):
        return self.bill_no


class BillDetails(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=False, related_name='BillDetails_bill')
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True, related_name='BillDetails_item')
    description = models.CharField(null=False,blank=False, max_length=500)
    qty = models.IntegerField(null=False,blank=False)
    unit_price = models.DecimalField(max_digits=30, decimal_places=6, null=False,blank=False)
    amount = models.DecimalField(max_digits=30, decimal_places=6, null=False, blank=False)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True, blank=True, related_name='BillDetails_tax')
    tax_amount = models.DecimalField(max_digits=30, decimal_places=6, null=False, blank=False, default=0)

    dr_account = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE, null=False, blank=False, related_name='BillDetails_dr_account')
    cr_account = models.ForeignKey(ChartOfAccount, on_delete=models.CASCADE, null=False, blank=False, related_name='BillDetails_cr_account')

    trnx_number = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, blank=True, related_name='BillDetails_trnx_number')

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=User, related_name='BillDetails_created_by')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='BillDetails_modified_by')
    updated_date = models.DateTimeField(null=True, blank=True, editable=False)

    # def save(self):
    #     self.amount = self.qty * self.unit_price
    #     super(BillDetails, self).save()

    def __str__(self):
        return self.bill.bill_no
