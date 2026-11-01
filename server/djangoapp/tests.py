from django.test import TestCase, Client
from django.contrib.auth.models import User
import json


class LoginLogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123',
            first_name='Test', last_name='User', email='test@example.com'
        )

    def test_login_valid(self):
        response = self.client.post(
            '/djangoapp/login',
            json.dumps({'userName': 'testuser', 'password': 'testpass123'}),
            content_type='application/json'
        )
        data = response.json()
        self.assertEqual(data['status'], 'Authenticated')

    def test_login_invalid(self):
        response = self.client.post(
            '/djangoapp/login',
            json.dumps({'userName': 'testuser', 'password': 'wrongpass'}),
            content_type='application/json'
        )
        data = response.json()
        self.assertEqual(data['status'], 'Failed')

    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/djangoapp/logout')
        data = response.json()
        self.assertEqual(data['userName'], '')
