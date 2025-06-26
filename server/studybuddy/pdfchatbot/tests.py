from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from authentication.models import User

# Create your tests here.

class PdfchatbotApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test5@example.com', password='testpass', is_student=True)
        self.client.force_authenticate(user=self.user)

    def test_health_check(self):
        response = self.client.get(reverse('pdfchatbot:pdfchatbot_health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'ok')

    def test_permissions(self):
        self.user.is_student = False
        self.user.is_senior = False
        self.user.save()
        response = self.client.get(reverse('pdfchatbot:pdfchatbot_health'))
        self.assertEqual(response.status_code, 403)
