from django.db import models
from django.conf import settings
from papers.models import Paper


class Keyword(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='keywords'
    )
    term = models.CharField(
        max_length=255,
        help_text="A single keyword or phrase to track."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user cannot subscribe to the exact same keyword twice.
        unique_together = ('user', 'term')
        ordering = ['term']

    def __str__(self):
        return f'{self.term} (User: {self.user.email})'


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    # Has the user seen this notification yet?
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user should only be notified about the same paper/keyword combo once.
        unique_together = ('user', 'paper', 'keyword')
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.email} on paper '{self.paper.title[:30]}...'"