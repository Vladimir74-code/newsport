from django.contrib import admin
from .models import News as Article



@admin.action(description="Mark selected stories as published")
def make_published(modeladmin, request, queryset):
    queryset.update(published=True)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "published"]
    ordering = ["title"]
    actions = [make_published]

admin.site.register(Article, ArticleAdmin)