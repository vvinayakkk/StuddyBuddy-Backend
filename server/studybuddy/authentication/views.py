from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .serializers import UserSerializer
from connections.models import FriendRequest
from connections.serializers import FriendRequestSerializer
from .managers import CustomUserManager
import jwt,datetime
from django.contrib.auth import authenticate, login
from django.conf import settings

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, email=email, password=password)

        if user and user.check_password(password):
            payload = {
                'id': user.id,
                'email': user.email, 
                'username': user.username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            print(payload)
            print(token)
            response = JsonResponse({'status': True, 'message': 'Login successful', 'token': token})
            decoded_token = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            print(decoded_token)
            return response

        return JsonResponse({'status': False, 'error': 'Invalid email or password'}, status=401)


class ProfileView(APIView):
    @login_required
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        friend_requests = FriendRequest.objects.filter(receiver=user, status='pending')
        friend_requests_serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response({
            'user': serializer.data,
            'friend_requests': friend_requests_serializer.data
        })

    @login_required
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcceptFriendRequestView(APIView):
    @login_required
    def post(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
        friend_request.status = 'accepted'
        friend_request.save()
        friend_request.sender.friends.add(request.user)
        request.user.friends.add(friend_request.sender)
        return JsonResponse({'message': 'Friend request accepted successfully'}, status=status.HTTP_200_OK)

class DeclineFriendRequestView(APIView):
    @login_required
    def post(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
        friend_request.status = 'declined'
        friend_request.save()
        return JsonResponse({'message': 'Friend request declined successfully'}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    @login_required
    def post(self, request):
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
