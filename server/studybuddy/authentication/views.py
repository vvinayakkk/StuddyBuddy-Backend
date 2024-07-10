from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime

class SignupView(APIView):
    def post(self, request):
        print("Received data:", request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("Signup dataset:", serializer.data)
            return JsonResponse({'message': 'Account created successfully'}, status=201)
        return JsonResponse(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            payload = {
                'id': user.id,
                'email': user.email, 
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')
            print(token)
            response = JsonResponse({'status': True, 'message': 'Login successful', 'token': token})
            return response

        return JsonResponse({'status': False, 'error': 'Invalid email or password'}, status=401)

class UniqueCheckView(APIView):
    def post(self, request):
        email = request.data.get('email')
        contact = request.data.get('contact')

        if User.objects.filter(email=email).exists() or User.objects.filter(contact=contact).exists():
            return JsonResponse({'status': False, 'message': 'Email or contact already exists'})

        return JsonResponse({'status': True, 'message': 'Email and contact are unique'})
