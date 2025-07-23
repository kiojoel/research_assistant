# papers/models.py
from django.db import models
from django.utils import timezone

class Paper(models.Model):
    # Core Metadata
    title = models.CharField(max_length=512)
    abstract = models.TextField()
    authors = models.JSONField(help_text="List of author names")

    # Source Information
    source = models.CharField(max_length=50, default='arxiv')
    source_id = models.CharField(
        max_length=100,
        unique=True,
        help_text="The paper's unique ID on its source platform (e.g., arXiv ID)"
    )

    # Links and Dates
    pdf_url = models.URLField(max_length=512)
    published_date = models.DateTimeField(default=timezone.now) # Use timezone.now as default

    # Timestamps for our use
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date'] # Show newest papers first by default

    def __str__(self):
        return self.title