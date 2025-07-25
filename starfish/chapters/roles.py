import logging

from django.utils.text import camel_case_to_spaces

logger = logging.getLogger(__name__)


class BaseRole:
    key = None
    label = None

    def __init__(self, chapter_role=None):
        self.chapter_role = chapter_role
        self.chapter = chapter_role.chapter
        super().__init__()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.key = camel_case_to_spaces(cls.__name__).replace(' ', '_')

    def has_perm(self, perm, obj=None):
        try:
            app_name, perm_name = perm.split('.')
        except ValueError:
            return False

        method_name = f'{app_name}_can_{perm_name}'
        logger.debug(f'call {method_name} {obj}')
        method = getattr(self, method_name, lambda obj: False)
        hp = bool(method(obj=obj))
        logger.debug(f'ret  {method_name}: {hp}')
        return hp

    def __str__(self):
        return self.label

    def get_allowed_member_fields(self, obj=None):
        fields = [
            'name',
        ]
        if self.members_can_view_email():
            fields.append('email')
        if self.members_can_view_phone():
            fields.append('phone')
        fields += [
            'zip_code',
            'chapter',
            'partner_campaign',
            'leadership_score',
            'referer_full',
            'validated',
        ]
        return fields

    def get_allowed_roles(self):
        return []

    def chapters_can_view_chapter(self, obj=None):
        return True

    def chapters_can_change_chapter(self, obj=None):
        return False

    def chapters_can_change_chapter_info(self, obj=None):
        return False

    def chapters_can_view_chapterrole(self, obj=None):
        return False

    def chapters_can_add_chapterrole(self, obj=None):
        return False

    def chapters_can_change_chapterrole(self, obj=None):
        return False

    def chapters_can_delete_chapterrole(self, obj=None):
        return type(obj) in self.get_allowed_role_classes()

    def members_can_view_member(self, obj=None):
        return True

    def members_can_view_email(self, obj=None):
        return False

    def members_can_view_phone(self, obj=None):
        return False

    def members_can_change_member(self, obj=None):
        return False

    def members_can_add_member(self, obj=None):
        return False


class ReporterEmail(BaseRole):
    label = 'Reporter (Email Only)'

    def members_can_view_email(self, obj=None):
        return True


class ReporterPhone(BaseRole):
    label = 'Reporter (Phone Only)'

    def members_can_view_phone(self, obj=None):
        return True


class Reporter(ReporterEmail, ReporterPhone):
    label = 'Reporter'

    def chapters_can_view_chapterrole(self, obj=None):
        return True


class Manager(Reporter):
    label = 'Manager'

    def chapters_can_change_chapter(self, obj=None):
        return True

    def members_can_change_member(self, obj=None):
        return self.chapter == obj.chapter

    def members_can_add_member(self, obj=None):
        return True

    def chapters_can_add_chapterrole(self, obj=None):
        return True

    def chapters_can_change_chapterrole(self, obj=None):
        return False

    def chapters_can_change_link(self, obj=None):
        return True

    def chapters_can_add_link(self, obj=None):
        return True

    def chapters_can_delete_link(self, obj=None):
        return True

    def get_allowed_roles(self):
        return ROLE_CHOICES.copy()[:-2]

    def get_allowed_role_classes(self):
        return _ROLE_CLASSES.copy()[:-2]


class Owner(Manager):
    label = 'Owner'

    def chapters_can_change_chapter_info(self, obj=None):
        return True

    def chapters_can_delete_chapterrole(self, obj=None):
        return True

    def get_allowed_roles(self):
        return ROLE_CHOICES

    def get_allowed_role_classes(self):
        return _ROLE_CLASSES


_ROLE_CLASSES = [ReporterEmail, ReporterPhone, Reporter, Manager, Owner]

ROLE_CLASSES = {cls.key: cls for cls in _ROLE_CLASSES}

ROLE_CHOICES = [(None, '---')] + [(cls.key, cls.label) for cls in _ROLE_CLASSES]


def get_role_instance(chapter_role):
    return ROLE_CLASSES.get(chapter_role.role_key)(chapter_role)
