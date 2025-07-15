from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates base groups'

    def handle(self, *args, **kwargs):
        cf, _ = Group.objects.get_or_create(name='Chapter Facilitators')

        perms = ['view_member', 'view_state', 'view_zip']
        cf.permissions.add(*[Permission.objects.get(codename=p) for p in perms])
