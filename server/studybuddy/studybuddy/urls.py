"""
URL configuration for studybuddy project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

try:
    from django_prometheus.exports import ExportToDjangoView
    prometheus_view = ExportToDjangoView
except ImportError:
    prometheus_view = lambda req: JsonResponse({"status": "prometheus disabled"})

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    
    # API v1 routes
    path('api/v1/pdfchatbot/', include('pdfchatbot.urls')),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/connect/', include('connections.urls')),
    path('api/v1/todolist/', include('todolist.urls')),
    path('api/v1/notes/', include('notes.urls')),
    path('api/v1/testseries/', include('testseries.urls')),
    path('api/v1/resources/', include('resources.urls')),

    # Direct / Root routes for direct frontend calls
    path('pdfchatbot/', include('pdfchatbot.urls')),
    path('connect/', include('connections.urls')),
    path('todolist/', include('todolist.urls')),
    path('notes/', include('notes.urls')),
    path('testseries/', include('testseries.urls')),
    path('resources/', include('resources.urls')),
    path('', include('authentication.urls')),

    path('metrics/', prometheus_view, name='metrics'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

