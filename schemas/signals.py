from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from schemas.tasks import generate_file
from schemas.models import DataSet


@receiver(post_save, sender=DataSet)
def dataset_generate(sender, instance, created, **kwargs):
    if created:
        generate_file.delay(instance.id)
