import arxiv
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from papers.models import Paper

class Command(BaseCommand):
    help = 'Fetches new papers from the arXiv API for a given category.'

    def handle(self, *args, **options):
        self.stdout.write("Starting to fetch papers from arXiv...")

        search = arxiv.Search(
            query="cat:cs.*",
            max_results=100,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        papers_added_count = 0
        for result in search.results():
            try:
                paper_source_id = result.entry_id.split('/')[-1]

                Paper.objects.create(
                    title=result.title,
                    abstract=result.summary,
                    authors=[author.name for author in result.authors],
                    source='arxiv',
                    source_id=paper_source_id,
                    pdf_url=result.pdf_url,
                    published_date=result.published,
                )
                papers_added_count += 1
                self.stdout.write(self.style.SUCCESS(f'Added: "{result.title[:60]}..."'))

            except IntegrityError:
                self.stdout.write(self.style.WARNING(f'Skipped (already exists): {result.title[:60]}...'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error processing paper {result.entry_id}: {e}'))

        self.stdout.write(self.style.SUCCESS(f"\nFinished fetching. Added {papers_added_count} new papers."))