from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from authentication.models import User
from .models import Resource

class ResourcesApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test4@example.com', password='testpass', is_student=True)
        self.client.force_authenticate(user=self.user)

    def test_health_check(self):
        response = self.client.get(reverse('resources:resources_health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'ok')

    def test_list_resources(self):
        Resource.objects.create(resource_type='pdf', url='http://example.com')
        response = self.client.get(reverse('resources:resource_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('results' in response.data)

    def test_permissions(self):
        self.user.is_student = False
        self.user.is_senior = False
        self.user.save()
        response = self.client.get(reverse('resources:resource_list'))
        self.assertEqual(response.status_code, 403)
