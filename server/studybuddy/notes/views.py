from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm, NoteShareForm
from authentication.models import User  
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import jwt
import logging

logger = logging.getLogger(__name__)

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
def note_list(request):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)
    
    notes = Note.objects.filter(shared_with=user) | Note.objects.filter(created_by=user)
    notes = notes.distinct()
    note_list = []
    for note in notes:
        note_list.append({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "image": note.image.url if note.image else None,
            "document": note.document.url if note.document else None,
            "rich_text_content": note.rich_text_content,
            "shared_with": [u.email for u in note.shared_with.all()]  # Include shared_with emails
        })
    
    return Response(note_list, status=status.HTTP_200_OK)

@api_view(['GET'])
def note_detail(request, pk):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)
    
    note = get_object_or_404(Note, pk=pk)
    if user not in note.shared_with.all() and user != note.created_by:
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    note_data = {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "image": note.image.url if note.image else None,
        "document": note.document.url if note.document else None,
        "rich_text_content": note.rich_text_content,
        "shared_with": [u.username for u in note.shared_with.all()]
    }
    return Response(note_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def note_create(request):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)
    print(user)
    data = request.data.copy()
    print(data)
    shared_with_ids = request.data.get('shared_with', [])
    print(shared_with_ids)
    # Ensure shared_with_ids is a list and contains valid user IDs
    if isinstance(shared_with_ids, list):
        shared_with_users = User.objects.filter(id__in=shared_with_ids)
        if shared_with_ids and len(shared_with_ids) != len(shared_with_users):
            return Response({"error": "One or more user IDs in shared_with are invalid"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        shared_with_users = []

    # Update data with valid shared_with users
    data['shared_with'] = [user.id for user in shared_with_users]
    print("hi")
    form = NoteForm(data, request.FILES, user=user)

    if form.is_valid():
        note = form.save(commit=False)
        note.created_by = user
        note.save()
        users_to_share_with = form.cleaned_data.get('shared_with')
        if users_to_share_with:
            note.shared_with.add(*users_to_share_with)
        return Response({"id": note.id, "title": note.title, "content": note.content, "image": note.image.url if note.image else None, "document": note.document.url if note.document else None, "rich_text_content": note.rich_text_content,"shared_with": [u.email for u in note.shared_with.all()]}, status=status.HTTP_201_CREATED)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def note_update(request, pk):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)
    
    note = get_object_or_404(Note, pk=pk)
    if user != note.created_by:
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    data = request.data.copy()
    new_shared_with = request.data.get('shared_with', [])
    
    # Retrieve existing shared_with users
    existing_shared_with = list(note.shared_with.all())
    
    # Update shared_with directly
    note.shared_with.clear()
    note.shared_with.add(*User.objects.filter(pk__in=new_shared_with))
    
    # Update other fields using the NoteForm as before
    form = NoteForm(data, request.FILES, instance=note, user=user)
    if form.is_valid():
        # Restore previous shared_with users if form validation succeeds
        note.shared_with.add(*existing_shared_with)
        
        note = form.save(commit=False)
        note.last_modified_by = user
        note.save()
        
        return Response({"id": note.id, "title": note.title, "content": note.content, "image": note.image.url if note.image else None, "document": note.document.url if note.document else None, "rich_text_content": note.rich_text_content,"shared_with": [u.email for u in note.shared_with.all()]}, status=status.HTTP_200_OK)
    else:
        # Restore previous shared_with users if form validation fails
        note.shared_with.add(*existing_shared_with)
        
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def note_share(request, pk):
    user, error, status_code = get_user_from_token(request)
    if user is None:
        logger.error(f"User could not be retrieved from token: {error}")
        return Response({"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
    note = get_object_or_404(Note, pk=pk)
    
    data = request.data.copy()
    user_ids = data.get('users', [])
    users = User.objects.filter(id__in=user_ids)
    
    if not users:
        return Response({"error": "No valid users found"}, status=status.HTTP_400_BAD_REQUEST)
    
    data['users'] = [user.pk for user in users] 
    
    if request.method == 'POST':
        form = NoteShareForm(data, note_instance=note, initial={'users': users})
        if form.is_valid():
            users_to_share_with = form.cleaned_data['users']
            note.shared_with.add(*users_to_share_with)
            return Response({"message": "Note shared successfully"}, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Form errors: {form.errors}")
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['DELETE'])
def note_delete(request, pk):
    user, error, status_code = get_user_from_token(request)
    if error:
        return Response(error, status=status_code)
    
    note = get_object_or_404(Note, pk=pk)
    if user != note.created_by:
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    note.delete()
    return Response({"message": "Note deleted successfully"}, status=status.HTTP_200_OK)
