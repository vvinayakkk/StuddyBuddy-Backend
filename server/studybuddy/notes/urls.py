from django.urls import path
from .views import NoteListView
from . import views

app_name = 'notes'

urlpatterns = [
    path('', NoteListView.as_view(), name="note_list"),
    path('<uuid:pk>/', views.note_detail, name="note_details"),
    path('create/', views.note_create, name="note_create"),
    path('<uuid:pk>/share/', views.note_share, name="note_share"),
    path('<uuid:pk>/update/', views.note_update, name="note_update"),
    path('<uuid:pk>/delete/', views.note_delete, name="note_delete"),
    path('health/', views.notes_health_check, name='notes_health'),
]
