import logging

from chapters.models import (
    Chapter,
    ChapterLink,
    ChapterRole,
    ChapterZip,
    OfflineTotal,
)
from django.contrib import admin
from django.forms import ModelForm
from django.urls import reverse
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import AutocompleteSelectMultipleFilter

from starfish.admin import SoftDeletableAdminMixin, pretty_button, pretty_links

logger = logging.getLogger(__name__)


class ChapterInlineMixin:

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        try:
            self.chapter_role = ChapterRole.objects.get(user=request.user, chapter=obj)
        except ChapterRole.DoesNotExist:
            self.chapter_role = None
        return super().get_formset(request, obj, **kwargs)

    def get_queryset(self, request):
        queryset = self.model._default_manager.get_queryset()
        if not self.has_view_or_change_permission(request, obj=self.parent_obj):
            queryset = queryset.none()
        return queryset

    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('chapters.view_chapter', obj=obj)

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('chapters.change_chapter_info', obj=obj)

    def has_add_permission(self, request, obj=None):
        return self.has_change_permission(request, obj=obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj=obj)


class ChapterZipInline(ChapterInlineMixin, TabularInline):
    model = ChapterZip
    fields = ['zip_code', 'county']
    autocomplete_fields = ['zip_code']
    extra = 1
    tab = True
    verbose_name = 'ZIP'
    readonly_fields = ['county']

    def county(self, obj):
        return obj.zip_code.county

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ChapterRoleInline(ChapterInlineMixin, TabularInline):
    model = ChapterRole
    readonly_fields = ['added_by_user']
    autocomplete_fields = ['user']
    extra = 1
    tab = True
    verbose_name = 'Role'

    def get_inline_title(self, obj):
        return ''

    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('chapters.view_chapterrole', obj=obj)

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('chapters.change_chapterrole', obj=obj)

    def has_add_permission(self, request, obj=None):
        return request.user.has_perm('chapters.add_chapterrole', obj=obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('chapters.delete_chapterrole', obj=obj)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if self.chapter_role and db_field.name == 'role_key':
            kwargs['choices'] = self.chapter_role.get_allowed_roles()
        return super().formfield_for_choice_field(db_field, request, **kwargs)


class ChapterLinkInlineForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs[
            'placeholder'
        ] = 'Leave blank to automatically generate title'

    def save(self, *args, **kwargs):
        if not self.instance.title:
            self.instance.set_title()
        return super().save(*args, **kwargs)


class ChapterLinkInline(ChapterInlineMixin, TabularInline):
    model = ChapterLink
    extra = 1
    tab = True
    verbose_name = 'Link'
    form = ChapterLinkInlineForm
    ordering_field = 'order'
    ordering = ['order']
    hide_ordering_field = True

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('chapters.change_link', obj=obj)

    def has_add_permission(self, request, obj=None):
        return request.user.has_perm('chapters.add_link', obj=obj)

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('chapters.delete_link', obj=obj)


class OfflineTotalInline(ChapterInlineMixin, TabularInline):
    model = OfflineTotal
    readonly_fields = ['submitted_by_user']
    extra = 1
    tab = True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Chapter)
class ChapterAdmin(SoftDeletableAdminMixin, SimpleHistoryAdmin, ModelAdmin):
    list_display = ('title', 'total_members', 'created')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ['title']}
    autocomplete_fields = ['nearby_chapters']
    readonly_fields = [
        'view_members_link',
    ]
    compressed_fields = True
    fields = [
        'state',
        'title',
        'slug',
        'nearby_chapters',
        'view_members_link',
        'description',
        'contact_email',
        'website_url',
        'organizing_hub_url',
    ]

    inlines = [
        ChapterRoleInline,
        ChapterLinkInline,
        OfflineTotalInline,
        ChapterZipInline,
    ]

    def view_members_link(self, obj):
        count = obj.members.count()
        return format_html(
            pretty_button(
                reverse('admin:members_member_changelist')
                + f'?chapter_id__exact={obj.id}',
                f'View {count} members',
                fmt=False,
            )
            + f' ({obj.total_members} total)'
        )

    view_members_link.short_description = 'Members'

    def nearby_chapters_display(self, obj):
        return pretty_links(
            (reverse('admin:chapters_chapter_change', args=[c.id]), c.title)
            for c in obj.nearby_chapters.all()
        )

    nearby_chapters_display.short_description = 'Nearby chapters'

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('chapters.change_chapter', obj=obj)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if isinstance(obj, OfflineTotal) and not obj.submitted_by_user_id:
                obj.submitted_by_user = request.user
            if isinstance(obj, ChapterRole) and not obj.added_by_user_id:
                obj.added_by_user = request.user
            obj.save()
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save_m2m()

    def get_fields(self, request, obj=None):
        fields = self.fields.copy()
        if not request.user.has_perm('chapters.change_chapter_info', obj=obj):
            fields[fields.index('nearby_chapters')] = 'nearby_chapters_display'
        if not request.user.has_perm('members.view_member', obj=obj):
            fields.pop(fields.index('view_members_link'))
        return fields

    def get_prepopulated_fields(self, request, obj=None):
        if obj and not request.user.has_perm('chapters.change_chapter_info', obj=obj):
            return {}
        return self.prepopulated_fields

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.has_perm('chapters.change_chapter_info', obj=obj):
            fields = [f.name for f in self.model._meta.fields] + [
                'nearby_chapters_display'
            ]
            if request.user.has_perm('members.view_member', obj=obj):
                fields += ['view_members_link']
            return fields
        return super().get_readonly_fields(request, obj)


@admin.register(ChapterZip)
class ChapterZipAdmin(ModelAdmin):
    list_display = [
        'zip_code',
        'chapter',
    ]
    search_fields = [
        'zip_code__code',
        'chapter__title',
    ]
    autocomplete_fields = ['chapter', 'zip_code']
    list_filter = [
        ('chapter', AutocompleteSelectMultipleFilter),
    ]
    fields = ['chapter', 'zip_code']
    compressed_fields = True
    list_filter_submit = True

    def state(self, obj):
        return obj.chapter.state

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return [field.name for field in obj._meta.fields]
        else:
            return []

    def has_change_permission(self, request, obj=None):
        return False
