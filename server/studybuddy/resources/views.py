from django.http import FileResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Resource
from .serializers import ResourceSerializer
from authentication.models import User
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import jwt
from rest_framework import generics, permissions, filters
from rest_framework.permissions import BasePermission

def get_user_from_token(request):
    try:
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None, {"error": "Authorization header missing"}, status.HTTP_401_UNAUTHORIZED
        
        token = authorization_header.split(' ')[1]
        decoded_token = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        
        user_id = decoded_token.get('id')
        if not user_id:
            return None, {"error": "Invalid token format"}, status.HTTP_403_FORBIDDEN
        
        user = get_object_or_404(User, id=user_id)
        return user, None, None
    except jwt.ExpiredSignatureError:
        return None, {"error": "Token has expired"}, status.HTTP_403_FORBIDDEN
    except jwt.DecodeError:
        return None, {"error": "Invalid token"}, status.HTTP_403_FORBIDDEN
    except Exception as e:
        return None, {"error": str(e)}, status.HTTP_403_FORBIDDEN

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Resource
from .serializers import ResourceSerializer
from authentication.views import get_user_from_token

class IsStudentOrSenior(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'is_student') and request.user.is_student or \
               hasattr(request.user, 'is_senior') and request.user.is_senior

class ResourceListView(generics.ListCreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOrSenior]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['resource_type', 'url']
    ordering_fields = ['id']
    ordering = ['-id']

    def get_queryset(self):
        return Resource.objects.all()

@api_view(['GET'])
def resources_health_check(request):
    return Response({'status': 'ok'}, status=200)
