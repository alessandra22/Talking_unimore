from django.test import Client
from django.urls import reverse
from django.test import TestCase


class HomePageTest(TestCase):
    def testHome(self):
        client = Client()
        response = client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
