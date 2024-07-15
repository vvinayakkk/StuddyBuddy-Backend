from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Room
from authentication.models import User
import jwt
from django.conf import settings

# Helper function to get user from the token
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
def rooms(request):
    user, error_response, status_code = get_user_from_token(request)
    if error_response:
        return Response(error_response, status=status_code)

    rooms = Room.objects.all()
    serialized_rooms = [{'id': room.id, 'name': room.name, 'slug': room.slug} for room in rooms]
    return Response({'rooms': serialized_rooms})

@api_view(['GET'])
def room(request, room_name):
    user, error_response, status_code = get_user_from_token(request)
    if error_response:
        return Response(error_response, status=status_code)

    username = user.username
    return Response({'room_name': room_name, 'username': username})
