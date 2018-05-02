# from unittest import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from ..backend.views import index


class TestUrlIndex(TestCase):
    def setUp(self):
        # Every test needs a client
        self.client = Client()

    def test_index(self):
        ind = index(self.client)
        reponse = self.client.get(reverse('../backend.views.index'))

        self.assertEqual(reponse.status_code, 200)
