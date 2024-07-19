from django.http import FileResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Resource, Bookmark
from .serializers import ResourceSerializer, BookmarkSerializer
from authentication.models import User
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import jwt

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

@api_view(['GET'])
def resource_list(request):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)
    
    resources = Resource.objects.all()
    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def resource_detail(request, pk):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)
    
    resource = get_object_or_404(Resource, pk=pk)
    serializer = ResourceSerializer(resource)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def resource_create(request):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)
    
    data = request.data.copy()
    data['created_by'] = user.id
    serializer = ResourceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def resource_bookmark(request, pk):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)
    
    resource = get_object_or_404(Resource, pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(user=user, resource=resource)
    if created:
        return Response({"status": "bookmarked"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"status": "already bookmarked"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def bookmark_list(request):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)
    
    bookmarks = Bookmark.objects.filter(user=user)
    serializer = BookmarkSerializer(bookmarks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def resource_download(request, pk):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)

    resource = get_object_or_404(Resource, pk=pk)
    if resource.resource_type == 'pdf' and resource.file:
        response = FileResponse(resource.file.open(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{resource.file.name}"'
        return response
    else:
        return Response({"error": "Resource not available for download"}, status=status.HTTP_400_BAD_REQUEST)
