from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Resource, Domain, UserResource
from .forms import ResourceForm
from django.shortcuts import get_object_or_404
from django.conf import settings
import jwt
from authentication.models import User
from django.http import FileResponse
from django.core.exceptions import ObjectDoesNotExist


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
def index(request):
    user, error, error_status = get_user_from_token(request)
    if error:
        return Response(error, status=error_status)

    resources = Resource.objects.all()
    user_resources = UserResource.objects.filter(user=user)
    saved_resource_ids = [user_resource.resource.uuid for user_resource in user_resources if user_resource.saved]
    domains = Domain.objects.all().order_by('name')

    response_data = {
        'resources': list(resources.values()),
        'saved_resource_ids': saved_resource_ids,
        'domains': list(domains.values())
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_page(request, resource_path):
    user, error, error_status = get_user_from_token(request)
    if error:
        return Response(error, status=error_status)

    resources = Resource.objects.all()
    user_resources = UserResource.objects.filter(user=user)
    saved_resource_ids = [user_resource.resource.uuid for user_resource in user_resources if user_resource.saved]
    domains = Domain.objects.all().order_by('name')

    response_data = {
        'resources': list(resources.values()),
        'saved_resource_ids': saved_resource_ids,
        'domains': list(domains.values())
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def file_page(request, resource_path, category):
    user, error, error_status = get_user_from_token(request)
    if error:
        return Response(error, status=error_status)

    resources = Resource.objects.filter(category=category)
    converted_resource_paths = [convert_to_lower_and_hyphen(resource.domain.name) for resource in resources]
    filtered_resources = [resource for resource, path in zip(resources, converted_resource_paths) if path == resource_path]

    user_resources = UserResource.objects.filter(user=user, resource__in=filtered_resources)
    saved_resource_ids = [user_resource.resource.uuid for user_resource in user_resources if user_resource.saved]

    resources_all = Resource.objects.all()
    user_resources_all = UserResource.objects.filter(user=user)
    saved_resource_ids_all = [user_resource.resource.uuid for user_resource in user_resources_all if user_resource.saved]
    domains = Domain.objects.all().order_by('name')

    response_data = {
        'resource_path': resource_path,
        'category': category,
        'resources': list(filtered_resources.values()),
        'saved_resource_ids': saved_resource_ids,
        'resources_all': list(resources_all.values()),
        'saved_resource_ids_all': saved_resource_ids_all,
        'domains': list(domains.values())
    }

    return Response(response_data, status=status.HTTP_200_OK)

def convert_to_lower_and_hyphen(domain_name):
    return domain_name.strip().replace(' ', '-').lower()

@api_view(['GET'])
def download_resource(request, resource_uuid):
    user, error, error_status = get_user_from_token(request)
    if error:
        return Response(error, status=error_status)

    resource = get_object_or_404(Resource, uuid=resource_uuid)
    file_path = resource.file.path  # Assuming your resource model has a 'file' field
    return FileResponse(open(file_path, 'rb'), as_attachment=True)

@api_view(['POST'])
def save_resource(request, resource_uuid):
    user, error, error_status = get_user_from_token(request)
    if error:
        return Response(error, status=error_status)

    resource = get_object_or_404(Resource, uuid=resource_uuid)
    user_resource, created = UserResource.objects.get_or_create(user=user, resource=resource)
    if not created:
        user_resource.saved = True
        user_resource.save()
    return Response({"message": "Resource saved successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def unsave_resource(request, resource_uuid):
    user, error, error_status = get_user_from_token(request)
    if error:
        return Response(error, status=error_status)

    resource = get_object_or_404(Resource, uuid=resource_uuid)
    user_resource = get_object_or_404(UserResource, user=user, resource=resource)
    user_resource.saved = False
    user_resource.save()
    return Response({"message": "Resource unsaved successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def res_form(request):
    user, error, error_status = get_user_from_token(request)
    if error:
        return Response(error, status=error_status)

    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploader = user

            domain_name = form.cleaned_data.get('domain')
            try:
                domain = Domain.objects.get(name=domain_name)
                resource.domain = domain
            except ObjectDoesNotExist:
                return Response({"error": "Domain does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            resource.save()
            return Response({"message": "Resource uploaded successfully"}, status=status.HTTP_201_CREATED)
    return Response({"error": "Invalid form data"}, status=status.HTTP_400_BAD_REQUEST)
