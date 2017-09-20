from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from organizations.models import Organization
from tax.forms import TaxForm, TaxComponentFormSet
from tax.models import TaxComponents, Tax


class TaxCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = TaxForm
    template_name = 'tax/tax_form.html'

    def get_success_url(self):
        return reverse_lazy('organizations:detail', kwargs={'pk': self.kwargs.get("org_id")})

    def get_form_kwargs(self):
        kwargs = super(TaxCreateView, self).get_form_kwargs()
        kwargs.update({'org_id': self.kwargs.get("org_id")})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TaxCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['tax_components'] = TaxComponentFormSet(self.request.POST)
        else:
            context['tax_components'] = TaxComponentFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        tax_components = context['tax_components']

        with transaction.atomic():
            organization = Organization.objects.filter(id=self.kwargs.get("org_id")).get()
            form.instance.org_id = organization
            form.instance.created_by = self.request.user
            form.instance.created_date = timezone.datetime.now()

            if tax_components.is_valid():

                # print('pass is valid')

                total_pct = 0
                compound_tax_pct = 0

                # print(self.request.POST)
                for i in range(0, int(self.request.POST['TaxComponents_tax-TOTAL_FORMS'])):
                    # compound = False
                    if self.request.POST['TaxComponents_tax-'+str(i)+'-component_desc']:
                        percentage = Decimal(self.request.POST['TaxComponents_tax-'+str(i)+'-percentage'])
                        try:
                            # print(self.request.POST['TaxComponents_tax-' + str(i) + '-compound'])
                            compound = True if self.request.POST['TaxComponents_tax-' + str(i) + '-compound'] == 'on' else False
                            # raise form.add_error('compound','hdhdhssh')
                            # return super(TaxCreateView, self).form_invalid(form)
                        except:
                            compound = False

                        if compound and compound_tax_pct == 0:
                            compound_tax_pct = percentage
                        elif compound and compound_tax_pct > 0:
                            return super(TaxCreateView, self).form_invalid(form)

                        self.object = form.save(commit=True)
                        tax_component = TaxComponents.objects.create(tax_id=self.object,
                                                                     component_desc=self.request.POST['TaxComponents_tax-'+str(i)+'-component_desc'],
                                                                     percentage=percentage,
                                                                     compound=compound,
                                                                     created_by=self.request.user,
                                                                     created_date=timezone.datetime.now())
                        total_pct += Decimal(self.request.POST['TaxComponents_tax-'+str(i)+'-percentage'])

                if compound_tax_pct > 0:
                    total_pct = (total_pct-compound_tax_pct)
                    form.instance.total_tax_pct = total_pct + (total_pct * (compound_tax_pct/100)) + compound_tax_pct
                else:
                    form.instance.total_tax_pct = total_pct
            else:
                return super(TaxCreateView, self).form_invalid(form)
        return super(TaxCreateView, self).form_valid(form)


class TaxUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = TaxForm
    template_name = 'tax/tax_form.html'

    def get_queryset(self):
        return Tax.objects.filter(id=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy('organizations:detail', kwargs={'pk': self.kwargs.get("org_id")})

    def get_form_kwargs(self):
        kwargs = super(TaxUpdateView, self).get_form_kwargs()
        kwargs.update({'org_id': self.kwargs.get("org_id")})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(TaxUpdateView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['tax_components'] = TaxComponentFormSet(self.request.POST,
                                                            instance=self.object,
                                                            form_kwargs={'user': self.request.user})
        else:
            context['tax_components'] = TaxComponentFormSet(instance=self.object,
                                                            form_kwargs={'user': self.request.user})
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        tax_components = context['tax_components']
        form.instance.modified_by = self.request.user
        form.instance.updated_date = timezone.datetime.now()

        # print('ssssssssssssssssssssssssssssssssssssss')
        # print(self.request.POST)
        # print('ssssssssssssssssssssssssssssssssssssss')
        # print(tax_components)
        # mutable = self.request.POST._mutable
        # self.request.POST._mutable = True
        # self.request.POST['TaxComponents_tax-' + str(0) + '-percentage'] = 99
        # print(self.request.POST['TaxComponents_tax-'+str(0)+'-percentage'])
        # self.request.POST._mutable = mutable
        # print('ssssssssssssssssssssssssssssssssssssss')
        if tax_components.is_valid():

            # print('pass is valid')

            total_pct = 0
            compound_tax_pct = 0

            # print(self.request.POST)
            self.object = form.save(commit=True)
            # tax_components.save(commit=True)

            for i in range(0, int(self.request.POST['TaxComponents_tax-TOTAL_FORMS'])):
                # compound = False
                if self.request.POST['TaxComponents_tax-' + str(i) + '-component_desc']:
                    percentage = Decimal(self.request.POST['TaxComponents_tax-' + str(i) + '-percentage'])
                    try:
                        # print(self.request.POST['TaxComponents_tax-' + str(i) + '-compound'])
                        compound = True if self.request.POST[
                                               'TaxComponents_tax-' + str(i) + '-compound'] == 'on' else False
                        # raise form.add_error('compound','hdhdhssh')
                        # return super(TaxCreateView, self).form_invalid(form)
                    except:
                        compound = False

                    if compound and compound_tax_pct == 0:
                        compound_tax_pct = percentage
                    elif compound and compound_tax_pct > 0:
                        return super(TaxUpdateView, self).form_invalid(form)

                    if self.request.POST['TaxComponents_tax-' + str(i) + '-id']:
                        tax_component = TaxComponents.objects.filter(id=int(self.request.POST['TaxComponents_tax-' + str(i) + '-id'])).\
                                                                     update(component_desc=self.request.POST['TaxComponents_tax-' + str(i) + '-component_desc'],
                                                                            percentage=percentage,
                                                                            compound=compound,
                                                                            modified_by=self.request.user,
                                                                            updated_date=timezone.datetime.now())
                    else:
                        tax_component = TaxComponents.objects.create(tax_id=self.object,
                                                                     component_desc=self.request.POST[
                                                                         'TaxComponents_tax-' + str(
                                                                             i) + '-component_desc'],
                                                                     percentage=percentage,
                                                                     compound=compound,
                                                                     created_by=self.request.user,
                                                                     created_date=timezone.datetime.now())

                    total_pct += Decimal(self.request.POST['TaxComponents_tax-' + str(i) + '-percentage'])

            if compound_tax_pct > 0:
                total_pct = (total_pct - compound_tax_pct)
                form.instance.total_tax_pct = total_pct + (total_pct * (compound_tax_pct / 100)) + compound_tax_pct
            else:
                form.instance.total_tax_pct = total_pct
        else:
            return super(TaxUpdateView, self).form_invalid(form)

        return super(TaxUpdateView, self).form_valid(form)


class TaxDetailView(LoginRequiredMixin,generic.DetailView):
    model = TaxForm
    template_name = "tax/tax_detail.html"