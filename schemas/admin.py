from django.contrib import admin
from schemas.models import Schema, SchemaColumn, DataSet


class SchemaColumnInline(admin.TabularInline):
    model = SchemaColumn
    extra = 0


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    inlines = [SchemaColumnInline]


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    pass
