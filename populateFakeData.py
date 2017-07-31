import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','AccountingProject.settings')
import django
django.setup()

import random
from AccountingApp.models import ChartOfAccounts, AccountTypes
from faker import Faker


fakgen = Faker()

account_types = ['Assets','Liabilities','Equity','Income','Expenses']


def add_account_types():
    print('Populating ... assets')
    assets = AccountTypes.objects.get_or_create(code='1',name=account_types[0])[0]
    print('Populating ... liabilities')
    liabilities = AccountTypes.objects.get_or_create(code='2', name=account_types[1])[0]
    print('Populating ... equity')
    equity = AccountTypes.objects.get_or_create(code='3', name=account_types[2])[0]
    print('Populating ... income')
    income = AccountTypes.objects.get_or_create(code='4', name=account_types[3])[0]
    print('Populating ... expenses')
    expenses = AccountTypes.objects.get_or_create(code='5', name=account_types[4])[0]

    #assets.save()
    #liabilities.save()
    #equity.save()
    #income.save()
    #expenses.save()

    return True

if __name__=='__main__':
    print('Populating ... ')
    add_account_types()
    print('Populating ... finished')






