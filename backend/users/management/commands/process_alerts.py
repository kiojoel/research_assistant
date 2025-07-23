from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from users.models import Keyword, Notification
from papers.models import Paper

class Command(BaseCommand):
    """
    This command processes all user-defined keywords and creates notifications
    for any new papers that match.
    """
    help = 'Processes keywords and creates notifications for matching papers.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Starting Alert Processing ---"))

        one_day_ago = timezone.now() - timedelta(days=1)
        recent_papers = Paper.objects.filter(created_at__gte=one_day_ago)

        if not recent_papers.exists():
            self.stdout.write("No new papers found in the last 24 hours. Exiting.")
            return

        self.stdout.write(f"Found {recent_papers.count()} recent papers to process.")


        all_keywords = Keyword.objects.all().select_related('user')

        if not all_keywords.exists():
            self.stdout.write("No keywords have been defined by any user. Exiting.")
            return

        self.stdout.write(f"Processing {all_keywords.count()} keywords...")
        notifications_created_count = 0

        for keyword in all_keywords:

            matching_papers = recent_papers.filter(
                Q(title__icontains=keyword.term) | Q(abstract__icontains=keyword.term)
            )


            for paper in matching_papers:

                notification, created = Notification.objects.get_or_create(
                    user=keyword.user,
                    paper=paper,
                    keyword=keyword
                )
                if created:
                    notifications_created_count += 1
                    # Log the successful creation to the console.
                    self.stdout.write(self.style.SUCCESS(
                        f"  + Match: '{keyword.term}' in paper '{paper.title[:30]}...' for {keyword.user.email}"
                    ))

        self.stdout.write(self.style.SUCCESS(f"\n--- Finished. Created {notifications_created_count} new notifications. ---"))