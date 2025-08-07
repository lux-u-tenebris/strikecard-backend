from django.urls import reverse_lazy

unfold_navigation = [
    {
        'collapsible': False,
        'items': [
            {
                'title': 'Chapters',
                'icon': 'groups',
                'link': reverse_lazy('admin:chapters_chapter_changelist'),
                'permission': lambda r: r.user.has_perm('chapters.view_chapter'),
            },
            {
                'title': 'Members',
                'icon': 'person',
                'link': reverse_lazy('admin:members_member_changelist'),
                'permission': lambda r: r.user.has_any_chapter_role(),
            },
            {
                'title': 'Partners',
                'icon': 'group',
                'link': reverse_lazy('admin:partners_partnercampaign_changelist'),
                'permission': lambda r: r.user.has_perm(
                    'partners.view_partnercampaign'
                ),
            },
            {
                'title': 'Affiliates',
                'icon': 'group',
                'link': reverse_lazy('admin:partners_affiliate_changelist'),
                'permission': lambda r: r.user.has_perm('partners.view_affiliate'),
            },
        ],
    },
    {
        'title': 'Regions',
        'collapsible': True,
        'items': [
            {
                'title': 'States',
                'icon': 'map',
                'link': reverse_lazy('admin:regions_state_changelist'),
                'permission': lambda r: r.user.has_perm('regions.view_state'),
            },
            {
                'title': 'ZIP Codes',
                'icon': 'map',
                'link': reverse_lazy('admin:regions_zip_changelist'),
                'permission': lambda r: r.user.has_perm('regions.view_zip'),
            },
            {
                'title': 'Chapter ZIPs',
                'icon': 'map',
                'link': reverse_lazy('admin:chapters_chapterzip_changelist'),
                'permission': lambda r: r.user.has_perm('regions.view_chapter_zip'),
            },
        ],
    },
    {
        'title': 'Access',
        'collapsible': True,
        'items': [
            {
                'title': 'Users',
                'icon': 'person',
                'link': reverse_lazy('admin:users_user_changelist'),
                'permission': lambda r: r.user.has_perm('users.view_user'),
            },
            {
                'title': 'Groups',
                'icon': 'group',
                'link': reverse_lazy('admin:auth_group_changelist'),
                'permission': lambda r: r.user.has_perm('users.view_group'),
            },
        ],
    },
]
