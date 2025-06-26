"""
URL configuration for studybuddy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from prometheus_django.views import ExportToDjangoView

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('api/v1/pdfchatbot/', include('pdfchatbot.urls')),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/connect/', include('connections.urls')),
    path('api/v1/todolist/', include('todolist.urls')),
    path('api/v1/notes/', include('notes.urls')),
    path('api/v1/testseries/', include('testseries.urls')),
    path('api/v1/resources/', include('resources.urls')),
    path('metrics/', ExportToDjangoView.as_view(), name='metrics'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
