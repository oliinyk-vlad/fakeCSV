from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit

from schemas.models import Schema, SchemaColumn, DataSet
from schemas.formsets import Formset


class SchemaColumnForm(forms.ModelForm):
    class Meta:
        model = SchemaColumn
        exclude = ()


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('name'),
                Field('column_separator'),
                Field('string_character'),
                Fieldset('Add columns',
                         Formset('columns')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
            )
        )


SchemaColumnFormSet = inlineformset_factory(
    Schema, SchemaColumn, form=SchemaColumnForm,
    fields=['name', 'type', 'order'], extra=1, can_delete=True
)


class DataSetForm(forms.ModelForm):
    class Meta:
        model = DataSet
        fields = ['rows']
