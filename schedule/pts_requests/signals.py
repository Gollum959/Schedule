from django.dispatch import receiver
from django.db.models.signals import post_delete

from pts_requests.models import PtsRequest


@receiver(post_delete, sender=PtsRequest)
def post_delete_cfg(sender, instance, *args, **kwargs):
    if instance.pts_cfg:
        instance.pts_cfg.delete()
