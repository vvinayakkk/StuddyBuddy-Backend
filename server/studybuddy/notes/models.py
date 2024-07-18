from django.db import models
from authentication.models import User
import uuid

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)  # Text content
    image = models.ImageField(upload_to='notes/images/', blank=True, null=True)  # Image upload
    document = models.FileField(upload_to='notes/documents/', blank=True, null=True)  # Document upload
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notes')
    shared_with = models.ManyToManyField(User, related_name='shared_notes')
    last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_notes')
    rich_text_content = models.TextField(blank=True, null=True)  # Rich text content

    def __str__(self):
        return self.title
