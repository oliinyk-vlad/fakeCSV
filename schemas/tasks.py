from __future__ import absolute_import, unicode_literals
from celery import task

from django.core.files.base import ContentFile
from io import StringIO

from schemas.models import DataSet
from schemas.common import DataNotFound, generate_row, generate_unreadable_row

import csv


@task()
def generate_file(dataset_id):
    dataset = DataSet.objects.get(id=dataset_id)
    filename = f'{dataset.schema.id}_{dataset.schema.name}.csv'
    fieldnames = [col.type for col in dataset.schema.schema_columns.order_by('order')]

    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer,
                            fieldnames=fieldnames,
                            delimiter=dataset.schema.column_separator,
                            quotechar=dataset.schema.string_character)
    writer.writeheader()
    for _ in range(dataset.rows):
        try:
            row = generate_row()
        except DataNotFound:
            row = generate_unreadable_row()
        writer.writerow({field: row.get(field) for field in fieldnames})

    csv_file = ContentFile(csv_buffer.getvalue().encode('utf-8'))

    dataset.status = 'ready'
    dataset.file.save(filename, csv_file)
    dataset.save()
