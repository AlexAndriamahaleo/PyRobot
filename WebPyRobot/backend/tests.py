import unittest
from django.test import Client
from django.contrib.auth.models import User
from .forms import *

# Create your tests here.


class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


# TODO: TESTS UNITAIRE
'''
class SignUpFormTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

        self.credentials = {
            'username' : 'testUserLogin',
            'password' : 'testUserLogin'
        }

        self.form = {
            'username': 'testUserLogin',
            'password': 'testUserLogin',
            'email': 'testUserLogin@email.com'
        }

        self.user = User.objects.create_user(self.form)

    def test_UserForm_valid(self):
        form = SignUpForm(data=self.form)
        self.assertTrue(form.is_valid())


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

        self.credentials = {
            'username' : 'testUserLogin',
            'password' : 'testUserLogin'
        }

        self.form = {
            'username': 'testUserLogin',
            'password': 'testUserLogin',
            'email': 'testUserLogin@email.com'
        }

        self.user = User.objects.create_user(self.form)

    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.client.login(username=self.credentials['username'], password=self.credentials['password'])
        self.assertEqual(response.status_code, 200)


class EditorTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

        self.credentials = {
            'username' : 'testUserLogin',
            'password' : 'testUserLogin'
        }

        self.form = {
            'username': 'testUserLogin',
            'password': 'testUserLogin',
            'email': 'testUserLogin@email.com'
        }

        self.user = User.objects.create_user(self.form)

    def editor_test(self):
        self.client.login(username=self.credentials['username'], password=self.credentials['password'])
        response = self.client.post('/editor/', self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)


class DocumentationTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

        self.credentials = {
            'username' : 'testUserLogin',
            'password' : 'testUserLogin'
        }

        self.form = {
            'username': 'testUserLogin',
            'password': 'testUserLogin',
            'email': 'testUserLogin@email.com'
        }

        self.user = User.objects.create_user(self.form)

    def documentation_test(self):
        self.client.login(username=self.credentials['username'], password=self.credentials['password'])
        response = self.client.post('/documentation/', self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)

'''