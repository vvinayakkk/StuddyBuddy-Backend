from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Domain, Resource, UserResource

class DomainAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'domain', 'uploader', 'upload_date')
    search_fields = ('title', 'description')
    list_filter = ('category', 'domain', 'upload_date')
    date_hierarchy = 'upload_date'
    ordering = ('-upload_date',)

class UserResourceAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'saved')
    search_fields = ('user__username', 'resource__title')
    list_filter = ('saved',)
    ordering = ('user', 'resource')

admin.site.register(Domain, DomainAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(UserResource, UserResourceAdmin)
