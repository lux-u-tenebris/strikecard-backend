import logging

from django.contrib.auth.backends import BaseBackend

from .models import Chapter, ChapterRole

logger = logging.getLogger(__name__)

FACILITATOR_PERMS = [
    'chapters.view_chapter',
    'chapters.view_role',
    'members.view_member',
    'regions.view_state',
    'regions.view_zip',
    'users.view_user',
]


class ChapterRolePermissionBackend(BaseBackend):

    def has_perm(self, user, perm, obj=None):
        if user.is_superuser:
            return True

        if perm in FACILITATOR_PERMS and user.has_any_chapter_role():
            return True

        if not obj:
            return super().has_perm(user, perm)

        logger.debug(f'backend {perm}')
        chapter = isinstance(obj, Chapter) and obj or getattr(obj, 'chapter')

        try:
            role = ChapterRole.objects.get(user=user, chapter=chapter)
        except ChapterRole.DoesNotExist:
            return False

        return role.has_perm(perm, obj=obj)
