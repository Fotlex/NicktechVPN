from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.servers.models import VpnServer
from backend.users.models import User


@receiver(post_save, sender=VpnServer)
def mailing_post_save(sender, instance: VpnServer, created, **kwargs):
    from backend.servers.tasks import add_client_to_server_task

    if created:
        users = User.objects.all()
        
        for user in users:
            transaction.on_commit(lambda: add_client_to_server_task.apply_async(args=[instance, user]))