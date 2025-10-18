from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.servers.models import VpnServer
from backend.users.models import User


@receiver(post_save, sender=VpnServer)
def server_post_save(sender, instance: VpnServer, created, **kwargs):
    from backend.servers.tasks import add_client_to_server_task

    if created:
        user_ids = User.objects.values_list('id', flat=True)
        
        for user_id in user_ids:
            transaction.on_commit(
                lambda u_id=user_id: add_client_to_server_task.apply_async(args=[u_id, instance.id])
            )