from django.contrib import admin
from .models import Resource, Bookmark

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'subject', 'subdomain', 'chapter', 'created_by', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource', 'created_at']
