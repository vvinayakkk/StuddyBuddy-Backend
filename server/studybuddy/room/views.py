# room/views.py

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Message
from authentication.models import User
from django.conf import settings
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
def room_list(request):
    rooms = Room.objects.all()
    return Response([{'id': room.id, 'name': room.name} for room in rooms], status=status.HTTP_200_OK)

@api_view(['GET'])
def room_messages(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages = room.messages.order_by('timestamp')
    return Response([
        {'user': message.user.username, 'content': message.content, 'timestamp': message.timestamp}
        for message in messages
    ], status=status.HTTP_200_OK)

@api_view(['POST'])
def create_room(request):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)

    room_name = request.data.get('name')
    if Room.objects.filter(name=room_name).exists():
        return Response({'error': 'Room already exists'}, status=status.HTTP_400_BAD_REQUEST)

    room = Room.objects.create(name=room_name)
    return Response({'id': room.id, 'name': room.name}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def send_message(request):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)

    room_id = request.data.get('room_id')
    content = request.data.get('content')
    room = get_object_or_404(Room, id=room_id)

    message = Message.objects.create(user=user, room=room, content=content)
    return Response({
        'user': message.user.username,
        'content': message.content,
        'timestamp': message.timestamp
    }, status=status.HTTP_201_CREATED)
