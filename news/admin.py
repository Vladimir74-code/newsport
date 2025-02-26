from django.contrib import admin
from .models import News

@admin.register(News)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'short_content', 'published_date', 'author']
    list_filter = ['published_date', 'author']

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content Preview'