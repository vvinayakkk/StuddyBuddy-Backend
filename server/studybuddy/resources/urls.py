from django.urls import path
from . import views

urlpatterns = [
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('resources/create/', views.resource_create, name='resource_create'),
    path('resources/<int:pk>/bookmark/', views.resource_bookmark, name='resource_bookmark'),
    path('bookmarks/', views.bookmark_list, name='bookmark_list'),
    path('resources/<int:pk>/download/', views.resource_download, name='resource_download'),
]
