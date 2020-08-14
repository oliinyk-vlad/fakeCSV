from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db import transaction

from schemas.models import Schema
from schemas.mixins import SchemaAccessMixin
from schemas.forms import DataSetForm, SchemaColumnFormSet, SchemaForm


class SchemaListView(LoginRequiredMixin, ListView):
    template_name = 'schemas/list.html'
    model = Schema

    def get_queryset(self):
        return Schema.objects.filter(user=self.request.user)


class SchemaCreateView(LoginRequiredMixin, CreateView):
    template_name = 'schemas/create.html'
    model = Schema
    form_class = SchemaForm

    def get_success_url(self):
        return reverse('schemas:detail', args=(self.object.id,))

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if columns.is_valid():
                columns.instance = self.object
                columns.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['columns'] = SchemaColumnFormSet(self.request.POST)
        else:
            data['columns'] = SchemaColumnFormSet()
        return data


class SchemaDetailView(LoginRequiredMixin, SchemaAccessMixin, FormView, DetailView):
    template_name = 'schemas/detail.html'
    model = Schema
    form_class = DataSetForm

    def get_context_data(self, **kwargs):
        context = super(SchemaDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_superuser and not request.user == self.object.user:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        dataset = form.save(commit=False)
        dataset.user = self.request.user
        dataset.schema = Schema.objects.get(id=self.object.id)
        dataset.save()

        return HttpResponseRedirect(reverse('schemas:detail', args=(self.object.id,)))


class SchemaUpdateView(LoginRequiredMixin, SchemaAccessMixin, UpdateView):
    template_name = 'schemas/update.html'
    model = Schema
    form_class = SchemaForm
    success_url = reverse_lazy('schemas:list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['columns'] = SchemaColumnFormSet(self.request.POST, instance=self.object)
        else:
            data['columns'] = SchemaColumnFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if columns.is_valid():
                columns.instance = self.object
                columns.save()
        return super().form_valid(form)


class SchemaDeleteView(LoginRequiredMixin, SchemaAccessMixin, DeleteView):
    template_name = 'schemas/delete.html'
    model = Schema
    success_url = reverse_lazy('schemas:list')
