from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import RequestContext
from django.core.urlresolvers import reverse

from AccountingApp.models import AccountTypes, ChartOfAccounts, ExchangeRate, Transactions, AccountTypesDrCr, Currencies
from AccountingApp.forms import UserForm, UserProfileInfoForm, ChartOfAccountsForm, TransactionsForm

from AccountingApp import forms
import django_excel as excel
from django import forms as djangoForms


class UploadFileForm(djangoForms.Form):
    file = djangoForms.FileField()


def register(request):
    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save User Form to Database
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()
            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)
    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

        # This is the render and context dictionary to feed
        # back to the registration.html file page.
    return render(request, 'AccountingApp/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'AccountingApp/login.html', {})


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('home'))


def get_exchange_rate(from_currency_id,to_currency_id):
    swap = 0
    if from_currency_id != to_currency_id:
        try:
            exchange_rate = ExchangeRate.objects.get(from_currency_id=from_currency_id,to_currency_id=to_currency_id)
        except ExchangeRate.DoesNotExist:
            try:
                exchange_rate = ExchangeRate.objects.get(from_currency_id=to_currency_id, to_currency_id=from_currency_id)
                swap = 1
            except ExchangeRate.DoesNotExist:
                exchange_rate = None

        if exchange_rate is not None:
            rate = exchange_rate.override_rate
            if swap == 0:
                return rate if rate > 0 else exchange_rate.rate
            else:
                return 1/rate if rate > 0 else 1/exchange_rate.rate
        else:
            return 0

    else:
        return 1


@login_required
def account_types(request):
    accountTypes_list = AccountTypes.objects.order_by('code')

    my_dict = {'accountTypes': accountTypes_list}

    return render(request, 'AccountingApp/account_types.html', context=my_dict)


@login_required
def get_account_by_code(request, code):

    account = ChartOfAccounts.objects.filter(code=code)
    my_dict = {'chartOfAccounts': account}

    return render(request, 'AccountingApp/chart_of_accounts_filter.html', context=my_dict)


def cancel(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_account_by_code(request, code):

    account = ChartOfAccounts.objects.get(code=code)
    chartOfAccounts_edit = forms.ChartOfAccountsForm(instance=account)

    if request.method == 'POST':
        chartOfAccounts_edit = forms.ChartOfAccountsForm(request.POST, instance=account)

        if chartOfAccounts_edit.is_valid():
            chartOfAccounts_edit.save(commit=True)
            return redirect('AccountingApp:chart_of_accounts')

    my_dict = {'chartOfAccounts': chartOfAccounts_edit, 'code': code}
    return render(request, 'AccountingApp/chart_of_accounts_edit.html', context=my_dict)


@login_required
def chart_of_accounts(request):
    chartOfAccounts_list = ChartOfAccounts.objects.order_by('type_code')

    my_dict = {'chartOfAccounts': chartOfAccounts_list}

    return render(request, 'AccountingApp/chart_of_accounts_all.html', context=my_dict)


@login_required
def chart_of_accounts_new(request):
    chartOfAccounts_new = forms.ChartOfAccountsForm()

    if request.method == 'POST':
        chartOfAccounts_new = forms.ChartOfAccountsForm(request.POST)

        if chartOfAccounts_new.is_valid():
            chartOfAccounts_new.save(commit=True)
            if 'save_add_another' in request.POST:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect('AccountingApp:chart_of_accounts')

    my_dict = {'chartOfAccounts': chartOfAccounts_new}
    return render(request, 'AccountingApp/chart_of_accounts_new.html', context=my_dict)


def home(request):
    return render(request, 'AccountingApp/home.html')


@login_required
def settings(request):
    return render(request, 'AccountingApp/settings.html')


def contactus(request):
    contact_us = forms.ContactUsForm()

    if request.method == 'POST':

        contact_us = forms.ContactUsForm(request.POST)

        if contact_us.is_valid():
            print("Form Validation Success. Prints in console.")
            contact_us.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'AccountingApp/contact_us.html', {'contact_us': contact_us})


@login_required
def add_transaction(request):
    transaction = forms.TransactionsForm()

    if request.method == 'POST':

        transaction = forms.TransactionsForm(request.POST)
        if transaction.is_valid():
            transaction.save(commit=True)
            if 'save_add_another' in request.POST:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect('AccountingApp:all_transactions')

    return render(request, 'AccountingApp/transactions_new.html', {'transaction': transaction})


def get_chart_of_accounts_type_code(account_code):
    return ChartOfAccounts.objects.get(code=account_code).type_code


def get_base_currency():
    return Currencies.objects.get(base_currency=True).currency_id


def validate_transaction(dr_account_code, cr_account_code):
    if dr_account_code != cr_account_code:
        dr_type_code = get_chart_of_accounts_type_code(dr_account_code)
        cr_type_code = get_chart_of_accounts_type_code(cr_account_code)

        dr_sign = AccountTypesDrCr.objects.get(code=dr_type_code, dr_cr=1)
        cr_sign = AccountTypesDrCr.objects.get(code=cr_type_code, dr_cr=2)

        if dr_sign.sign == cr_sign.sign:
            return False
        else:
            return True
    else:
        return False


@login_required
def all_transactions(request):
    transactions = Transactions.objects.order_by('transaction_id')

    my_dict = {'transactions': transactions}

    return render(request, 'AccountingApp/transactions_all.html', context=my_dict)


@login_required
def get_transaction_by_id(request, transaction_id):
    transaction = Transactions.objects.filter(transaction_id=transaction_id)
    my_dict = {'transactions': transaction}

    return render(request, 'AccountingApp/transactions_filter.html', context=my_dict)


@login_required
def edit_transaction_by_id(request, transaction_id):
    transaction = Transactions.objects.get(transaction_id=transaction_id)
    transaction_edit = forms.TransactionsForm(instance=transaction)

    if request.method == 'POST':
        transaction_edit = forms.TransactionsForm(request.POST, instance=transaction)

        if transaction_edit.is_valid():
            transaction_edit.save(commit=True)
            return redirect('AccountingApp:all_transactions')

    my_dict = {'transaction': transaction_edit, 'transaction_id': transaction_id}
    return render(request, 'AccountingApp/transactions_edit.html', context=my_dict)


@login_required
def export_data(request, atype):
    if atype == "sheet":
        return excel.make_response_from_a_table(
            AccountTypes, 'xls', file_name="sheet")
    elif atype == "book":
        return excel.make_response_from_tables(
            [Transactions, ChartOfAccounts], 'xls', file_name="book")
    elif atype == "custom":
        account_type = AccountTypes.objects.get(code=1)
        chart_of_account = ChartOfAccounts.objects.filter(type_code=account_type)
        column_names = ['code', 'name', 'type_code', 'main_code']
        return excel.make_response_from_query_sets(
            chart_of_account,
            column_names,
            'xls',
            file_name="custom"
        )
    else:
        return HttpResponseBadRequest(
            "Bad request. please put one of these " +
            "in your url suffix: sheet, book or custom")


@login_required
def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            request.FILES['file'].save_to_database(
                name_columns_by_row=0,
                model=AccountTypes,
                mapdict=['code', 'id', 'main_code_id', 'name'])
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'AccountingApp/upload_form.html',
        {'form': form})


@login_required
def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)

        def choice_func(row):
            q = AccountTypes.objects.filter(slug=row[0])[0]
            row[0] = q
            return row
        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[AccountTypes, ChartOfAccounts],
                initializers=[None, choice_func],
                mapdicts=[
                    ['code', 'name', 'main_code'],
                    ['code', 'name', 'type_code', 'main_code']]
            )
            return redirect('handson_view')
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'AccountingApp/upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        })


def handson_table(request):
    return excel.make_response_from_tables(
        [AccountTypes, ChartOfAccounts], 'handsontable.html')


