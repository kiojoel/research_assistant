from django.contrib import admin
from .models import Paper

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'published_date', 'created_at')
    list_filter = ('source', 'published_date')
    search_fields = ('title', 'abstract', 'source_id')
    date_hierarchy = 'published_date'