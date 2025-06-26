from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from authentication.models import User
from .models import Note

class NotesApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='testpass', is_student=True)
        self.client.force_authenticate(user=self.user)

    def test_health_check(self):
        response = self.client.get(reverse('notes:notes_health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'ok')

    def test_list_notes(self):
        Note.objects.create(title='Test Note', content='Test', created_by=self.user)
        response = self.client.get(reverse('notes:note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('results' in response.data)

    def test_permissions(self):
        self.user.is_student = False
        self.user.is_senior = False
        self.user.save()
        response = self.client.get(reverse('notes:note_list'))
        self.assertEqual(response.status_code, 403)
