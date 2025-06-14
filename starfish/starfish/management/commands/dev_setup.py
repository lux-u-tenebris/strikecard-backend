import random

from chapters.models import Chapter
from chapters.tests.factories import (
    ChapterRoleFactory,
    ChapterSocialLinkFactory,
    OfflineTotalFactory,
)
from contacts.tests.factories import (
    ContactFactory,
    ExpungedContactFactory,
    PendingContactFactory,
    RemovedContactFactory,
)
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from partners.tests.factories import (
    AffiliateFactory,
    PartnerCampaignFactory,
    PledgeFactory,
)
from users.tests.factories import UserFactory


class Command(BaseCommand):
    help = 'Setup default dev data'

    def get_partner_campaign(self, threshold=0.2):
        if random.random() < threshold:
            return random.choice(self.partner_campaigns)
        return None

    def handle(self, *args, **kwargs):
        User = get_user_model()

        admin = User.objects.filter(username='admin').first()
        if not admin:
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'a')

        self.partner_campaigns = []
        for _ in range(5):
            pc = PartnerCampaignFactory()
            self.partner_campaigns.append(pc)

        for _ in range(3):
            affiliate = AffiliateFactory()
            for _ in range(2):
                PledgeFactory(affiliate=affiliate, submitted_by_user=admin)

        for chapter in Chapter.objects.all():
            users = []
            for _ in range(2):
                user = UserFactory()
                users.append(user)
                ChapterRoleFactory(chapter=chapter, user=user, added_by_user=admin)

            for _ in range(4):
                ChapterSocialLinkFactory(chapter=chapter)

            for _ in range(random.randint(0, 2)):
                OfflineTotalFactory(
                    chapter=chapter, submitted_by_user=random.choice(users)
                )

            for _ in range(random.randint(0, 3)):
                PendingContactFactory(
                    chapter=chapter, partner_campaign=self.get_partner_campaign()
                )

            for _ in range(random.randint(0, 3)):
                RemovedContactFactory(removed_by=random.choice(users))

            for _ in range(random.randint(0, 3)):
                ExpungedContactFactory(
                    chapter=chapter, partner_campaign=self.get_partner_campaign()
                )

        for _ in range(1000):
            ContactFactory(partner_campaign=self.get_partner_campaign())
