from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from connections.models import FriendRequest
from .managers import CustomUserManager

DEPARTMENT_CHOICES = [
    ('CSE', 'Computer Science'),
    ('EXTC', 'Electronics and Telecommunication'),
    ('MCA', 'Master of Computer Applications'),
    ('CE', 'Civil Engineering'),
]

YEAR_CHOICES = [
    ('1', 'First Year'),
    ('2', 'Second Year'),
    ('3', 'Third Year'),
    ('4', 'Fourth Year'),
]

AVAILABILITY_CHOICES = [
    ('Morning', _('Morning')),
    ('Evening', _('Evening')),
    ('Night', _('Night')),
]


class User(AbstractUser):
    objects=CustomUserManager()
    email = models.EmailField(unique=True)
    username=models.CharField(max_length=150,unique=True,null=True,blank=True)
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES, blank=True)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES, blank=True)
    availability = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES, blank=True)
    courses = models.CharField(max_length=6, blank=True)
    preferred_study_methods = models.TextField(blank=True)
    goals = models.TextField(blank=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=False)


   

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions '
                    'granted to each of their groups.'),
        verbose_name=_('groups')
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions')
    )

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email
