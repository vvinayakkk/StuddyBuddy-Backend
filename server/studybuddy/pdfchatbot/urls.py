from django.urls import path
from . import views
from rest_framework.permissions import IsAuthenticated
from .views import pdfchatbot_health_check

urlpatterns = [
    path('health/', pdfchatbot_health_check, name='pdfchatbot_health'),
    path('upload_pdfs/', views.upload_pdfs, name='upload_pdfs'),
    path('ask_question/', views.ask_question, name='ask_question'),
    path('chat/', views.chat, name='chat'),
]