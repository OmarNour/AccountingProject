from django.contrib import admin

from bill.models import Bill,BillDetails

admin.site.register(Bill)
admin.site.register(BillDetails)
