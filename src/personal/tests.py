from django.test import LiveServerTestCase
from django.urls import reverse


class IntegrationTests(LiveServerTestCase):
    def test_contact(self):
        response = self.client.get(reverse('personal:contact'))
        self.assertEqual(response.status_code, 200)
