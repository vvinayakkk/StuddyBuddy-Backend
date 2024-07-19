from django.db import models
from authentication.models import User
from testseries.models import Subject, Subdomain, Chapter  # Assuming these models are in the testseries app

class Resource(models.Model):
    RESOURCE_TYPES = (
        ('youtube', 'YouTube Link'),
        ('pdf', 'PDF File'),
        ('link', 'Anonymous Link'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    url = models.URLField(blank=True, null=True)  # For YouTube and anonymous links
    file = models.FileField(upload_to='resources/files/', blank=True, null=True)  # For PDF files
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    subdomain = models.ForeignKey(Subdomain, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bookmarked {self.resource.title}"
