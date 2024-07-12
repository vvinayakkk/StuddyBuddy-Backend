from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Selfstudy, Assignment
from .serializers import SelfstudySerializer, AssignmentSerializer
from datetime import datetime
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def index(request):
    return Response({"message": "Welcome to the TodoList API!"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def assignments(request):
    assignments = Assignment.objects.filter(user=request.user)
    currentTime = datetime.now().replace(tzinfo=None)
    for a in assignments:
        if a.due_date is not None:
            a.is_before_due_date = a.due_date.replace(tzinfo=None) < currentTime
        else:
            a.is_before_due_date = False
    serializer = AssignmentSerializer(assignments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def selfstudy(request):
    selfstudy = Selfstudy.objects.filter(user=request.user)
    currentTime = datetime.now().replace(tzinfo=None)
    for s in selfstudy:
        if s.due_date is not None:
            s.is_before_due_date = s.due_date.replace(tzinfo=None) < currentTime
        else:
            s.is_before_due_date = False
    serializer = SelfstudySerializer(selfstudy, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_assignments(request):
    serializer = AssignmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_selfstudy(request):
    serializer = SelfstudySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_selfstudy(request, uuid):
    selfstudy = get_object_or_404(Selfstudy, uuid=uuid, user=request.user)
    selfstudy.completed = True
    selfstudy.save()
    return Response({"message": "Self-study marked as completed"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_assignments(request, uuid):
    assignment = get_object_or_404(Assignment, uuid=uuid, user=request.user)
    assignment.completed = True
    assignment.save()
    return Response({"message": "Assignment marked as completed"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_selfstudy(request, uuid):
    selfstudy = get_object_or_404(Selfstudy, uuid=uuid, user=request.user)
    selfstudy.delete()
    return Response({"message": "Self-study deleted"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_assignments(request, uuid):
    assignment = get_object_or_404(Assignment, uuid=uuid, user=request.user)
    assignment.delete()
    return Response({"message": "Assignment deleted"}, status=status.HTTP_200_OK)
