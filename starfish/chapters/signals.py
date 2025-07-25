from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import ChapterRole, OfflineTotal


@receiver([post_save, post_delete], sender=OfflineTotal)
def update_chapter_total_on_offline_total_change(sender, instance, **kwargs):
    instance.chapter.update_total_members()


@receiver([post_save, post_delete], sender=ChapterRole)
def update_facilitator_group_placement_on_chapter_role_change(
    sender, instance, **kwargs
):
    instance.user.facilitator_group_placement()
