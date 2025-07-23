# users/admin.py
from django.contrib import admin
from .models import Keyword, Notification

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('term', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('term',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('paper_title', 'user', 'keyword', 'is_read', 'created_at')
    list_filter = ('is_read', 'user', 'keyword')

    # A helper method to display the paper's title
    def paper_title(self, obj):
        return obj.paper.title