from chapters.models import (
    Chapter,
    ChapterRole,
    ChapterSocialLink,
    ChapterZip,
    OfflineTotal,
)
from django.contrib import admin
from django.urls import reverse
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import AutocompleteSelectMultipleFilter

from starfish.admin import SoftDeletableAdminMixin, pretty_button, pretty_links


class ChapterInlineMixin:

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
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


class ChapterSocialLinkInline(ChapterInlineMixin, TabularInline):
    model = ChapterSocialLink
    extra = 1
    tab = True
    verbose_name = 'Link'


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
    ]
    inlines = [
        ChapterRoleInline,
        ChapterSocialLinkInline,
        OfflineTotalInline,
        ChapterZipInline,
    ]

    def view_members_link(self, obj):
        return pretty_button(
            reverse('admin:members_member_changelist') + f'?chapter_id__exact={obj.id}',
            f'View {obj.total_members} members',
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
