from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AccountViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='student@example.com',
            username='student1',
            password='StrongPass123!',
            last_name='Doe',
            first_name='John',
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_blocks_authenticated_users(self):
        self.client.login(email='student@example.com', password='StrongPass123!')
        response = self.client.get(reverse('register'))
        self.assertIn(response.status_code, (302, 403))

    def test_profile_page_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)