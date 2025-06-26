# resources/urls.py
from django.urls import path
from .views import ResourceListView, resources_health_check
from . import views

urlpatterns = [
    path('', ResourceListView.as_view(), name='resource_list'),
    path('health/', resources_health_check, name='resources_health'),
    path('resources/', views.resource_list, name='resource-list'),
]
