from django.contrib import admin

from AccountingApp.models import AccountTypes, ChartOfAccounts, ContactUs, UserProfileInfo, Currencies, ExchangeRate,\
    DrCr, Transactions, Sign, AccountTypesDrCr


admin.site.register(AccountTypes)
admin.site.register(ChartOfAccounts)
admin.site.register(ContactUs)
admin.site.register(UserProfileInfo)
admin.site.register(Currencies)
admin.site.register(ExchangeRate)
admin.site.register(DrCr)
admin.site.register(Transactions)
admin.site.register(Sign)
admin.site.register(AccountTypesDrCr)
