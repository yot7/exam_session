from django.test import TestCase
from django.urls import reverse


class CommonViewsTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('common:home'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page_loads(self):
        response = self.client.get(reverse('common:dashboard'))
        self.assertEqual(response.status_code, 200)