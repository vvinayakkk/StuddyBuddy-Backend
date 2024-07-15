from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'last_modified_by']
    search_fields = ['title', 'content', 'created_by__username', 'last_modified_by__username']
