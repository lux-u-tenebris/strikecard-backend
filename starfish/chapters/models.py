import logging
import urllib.parse

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Sum
from django.utils.functional import cached_property
from model_utils.models import SoftDeletableModel, TimeStampedModel
from regions.models import State, Zip
from simple_history.models import HistoricalRecords

from starfish.helpers.link_title_parser import LinkTitleParser
from starfish.models import SoftDeletablePermissionManager

from .roles import ROLE_CHOICES, ROLE_CLASSES, get_role_instance

logger = logging.getLogger(__name__)


def get_chapter_for_zip(zip_code):
    if not zip_code:
        return None

    if isinstance(zip_code, str):
        zip_code = Zip.objects.get(code=zip_code)

    try:
        return ChapterZip.objects.get(zip_code=zip_code.code).chapter
    except (ChapterZip.DoesNotExist, Chapter.DoesNotExist):
        try:
            return Chapter.objects.filter(state=zip_code.state_id).first()
        except Chapter.DoesNotExist:
            return None


class Chapter(TimeStampedModel, SoftDeletableModel):
    state = models.ForeignKey(State, related_name='chapters', on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    website_url = models.URLField('Website', blank=True, null=True)
    nearby_chapters = models.ManyToManyField('self', blank=True)
    total_members = models.IntegerField(default=0)
    organizing_hub_url = models.URLField('Organizing Hub', blank=True, null=True)

    objects = SoftDeletablePermissionManager()
    history = HistoricalRecords()

    class Meta:
        ordering = (
            'state__name',
            'title',
        )

    def __str__(self):
        return self.title

    def update_total_members(self, save=True):
        self.total_members = (
            self.members.count()
            + (self.offline_totals.aggregate(Sum('count'))['count__sum'] or 0)
            + self.expunged_members.count()
        )
        if save:
            self.save()


class ChapterRole(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='chapter_roles'
    )
    added_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='added_roles',
        editable=False,
    )
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT, related_name='roles')
    role_key = models.CharField(
        verbose_name='Role', max_length=20, choices=ROLE_CHOICES
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'chapter'], name='chapter_role_unique_user_role'
            ),
            models.CheckConstraint(
                check=Q(role_key__in=ROLE_CLASSES.keys()), name='valid_role_key_check'
            ),
        ]

    def __str__(self):
        return str(self.role)

    @cached_property
    def role(self):
        return get_role_instance(self)

    def has_perm(self, perm, obj=None):
        return self.role.has_perm(perm, obj=obj)

    def get_allowed_roles(self):
        return self.role.get_allowed_roles()

    def get_allowed_member_fields(self):
        return self.role.get_allowed_member_fields()


class ChapterLink(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT, related_name='links')
    url = models.URLField('URL')
    # Do not show title on creation
    # Populate from entered URL by resolving HTTP request
    # Allow editing
    title = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField('Order', default=0, db_index=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.url

    def initial_title_text(self):
        return 'We will try to figure out a title for you :)'

    def save(self, *args, **kwargs):
        if (
            not self.title or self.title == self.initial_title_text()
        ) and self._state.adding:
            logger.info(f'Searching for link title for {self}')
            self.get_link_title_from_url()
        super().save(*args, **kwargs)

    @property
    def link_hostname(self):
        if self.url is None or len(self.url) == 0:
            return ''
        return urllib.parse.urlsplit(self.url).netloc

    def get_link_title_from_url(self):
        parser = LinkTitleParser(self.url)
        self.title = parser.title_content


class ChapterZip(models.Model):
    zip_code = models.OneToOneField(
        Zip,
        primary_key=True,
        on_delete=models.PROTECT,
        related_name='chapter',
        verbose_name='ZIP',
    )
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT, related_name='zips')

    class Meta:
        verbose_name = 'Chapter ZIP'
        ordering = ('zip_code',)

    def __str__(self):
        return str(self.zip_code)

    def clean(self):
        if self.chapter_id and self.zip_code_id:
            if self.chapter.state != self.zip_code.state:
                raise ValidationError(
                    'ZIP code must be in the same state as the chapter.'
                )


class OfflineTotal(models.Model):
    chapter = models.ForeignKey(
        Chapter, on_delete=models.PROTECT, related_name='offline_totals'
    )
    count = models.PositiveIntegerField()
    submitted_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, editable=False
    )
    notes = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.created.strftime('%b %d, %Y')
