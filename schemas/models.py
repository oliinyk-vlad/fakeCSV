from django.db import models
from django.conf import settings


class Schema(models.Model):
    COLUMN_SEPARATOR_CHOICES = (
        (",", "Comma (,)"),
        (";", "Semicolon (;)"),
        ("|", "Pipe (|)"),
    )

    STRING_CHARACTER_CHOICES = (
        ('"', 'Double-quote (")'),
        ("*", "Asterisk (*)"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    column_separator = models.CharField(max_length=10, default=',', choices=COLUMN_SEPARATOR_CHOICES)
    string_character = models.CharField(max_length=10, default='"', choices=STRING_CHARACTER_CHOICES)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)


class SchemaColumn(models.Model):
    COLUMN_TYPE = (
        ("full_name", "Full name"),
        ("email", "Email"),
        ("domain_name", "Domain name"),
        ("phone_number", "Phone number"),
        ("company_name", "Company Name"),
        ("address", "Address"),
    )
    schema = models.ForeignKey(Schema, related_name='schema_columns', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=COLUMN_TYPE)
    order = models.PositiveIntegerField(default=0)


class DataSet(models.Model):
    SCHEMA_TYPE = (
        ("processing", "Processing"),
        ("ready", "Ready"),
    )

    schema = models.ForeignKey(Schema, related_name='datasets', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    rows = models.PositiveIntegerField(default=10)
    status = models.CharField(max_length=255, default='processing', choices=SCHEMA_TYPE)
    file = models.FileField(blank=True, null=True)
