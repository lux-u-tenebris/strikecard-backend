from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

cf_perms = [
    'view_chapter',
    'view_member',
    'view_state',
    'view_zip',
    'view_user',
    'view_role',
]


class Command(BaseCommand):
    help = 'Creates base groups'

    def handle(self, *args, **kwargs):
        cf, _ = Group.objects.get_or_create(name='Chapter Facilitators')

        cf.permissions.add(*[Permission.objects.get(codename=p) for p in cf_perms])
