from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime


class Domain(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Resource(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STUDY_GUIDES = 'Study Guides'
    LECTURE_NOTES = 'Lecture Notes'
    PRACTICE_EXAMS = 'Practice Exams'
    USEFUL_WEBSITES = 'Useful Websites'

    CATEGORY_CHOICES = [
        (STUDY_GUIDES, 'Study Guides'),
        (LECTURE_NOTES, 'Lecture Notes'),
        (PRACTICE_EXAMS, 'Practice Exams'),
        (USEFUL_WEBSITES, 'Useful Websites'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resources/')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.title
    
 
    

class UserResource(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='domains')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='interests')
    saved = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'resource']

