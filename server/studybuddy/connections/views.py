from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import FriendRequest, Message
from .serializers import FriendRequestSerializer, MessageSerializer
from authentication.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@login_required(login_url='authentication:login')
def connect(request):
    user_profiles = User.objects.exclude(id=request.user.id)
    current_user_friends_ids = request.user.friends.values_list('id', flat=True)
    user_profiles = user_profiles.exclude(id__in=current_user_friends_ids)

    courses = request.GET.get('courses')
    search_query = request.GET.get('search')
    availability = request.GET.get('availability')

    if search_query:
        user_profiles = user_profiles.filter(username__icontains=search_query)
    
    if courses:
        user_profiles = user_profiles.filter(courses=courses)
    
    if availability:
        user_profiles = user_profiles.filter(availability=availability)

    current_user = request.user
    for profile in user_profiles:
        profile.has_pending_request = FriendRequest.objects.filter(sender=current_user, receiver=profile).exists()
        profile.is_friend = current_user.friends.filter(id=profile.id).exists()

    serialized_profiles = []
    for profile in user_profiles:
        serialized_profiles.append({
            'id': profile.id,
            'username': profile.username,
            'email': profile.email,
            'department': profile.department,
            'year': profile.year,
            'availability': profile.availability,
            'courses': profile.courses,
            'preferred_study_methods': profile.preferred_study_methods,
            'goals': profile.goals,
            'has_pending_request': profile.has_pending_request,
            'is_friend': profile.is_friend,
        })

    return Response({
        'students': serialized_profiles,
    })

@method_decorator(csrf_exempt, name='dispatch')
class SendFriendRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, receiver_id):
        receiver = get_object_or_404(User, id=receiver_id)
        sender = request.user
        existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver).exists()
        if not existing_request:
            FriendRequest.objects.create(sender=sender, receiver=receiver)
            return Response({'message': 'Friend request sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='authentication:login')
def friends(request):
    user = request.user
    friends = user.friends.all()

    serialized_friends = []
    for friend in friends:
        serialized_friends.append({
            'id': friend.id,
            'username': friend.username,
            'email': friend.email,
            'department': friend.department,
            'year': friend.year,
            'availability': friend.availability,
            'courses': friend.courses,
            'preferred_study_methods': friend.preferred_study_methods,
            'goals': friend.goals,
        })

    return Response({
        'friends': serialized_friends,
    })

@login_required(login_url='authentication:login')
def chat(request, username):
    recipient = get_object_or_404(User, username=username)
    if request.method == 'POST':
        content = request.data.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=recipient, content=content)
            return Response({'message': 'Message sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Content cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        messages_history = Message.objects.filter(sender=request.user, receiver=recipient) | Message.objects.filter(sender=recipient, receiver=request.user)
        serialized_messages = []
        for message in messages_history:
            serialized_messages.append({
                'id': message.id,
                'sender': message.sender.username,
                'receiver': message.receiver.username,
                'content': message.content,
                'timestamp': message.timestamp,
            })
        return Response({
            'recipient': recipient.username,
            'messages': serialized_messages,
        })

@login_required(login_url='authentication:login')
def videocall(request):
    username = request.user.username
    return Response({'username': username})

@login_required(login_url='authentication:login')
def joinmeet(request):
    if request.method == 'POST':
        rid = request.data.get('roomID')
        return Response({'roomID': rid})
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
