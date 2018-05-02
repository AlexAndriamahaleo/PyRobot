from unittest import TestCase
from django.test import Client, SimpleTestCase
from django.contrib.auth.models import User
from .forms import *

# Create your tests here.


# class SimpleTest(TestCase):
#    def setUp(self):
#        # Every test needs a client.
#        self.client = Client()

#     def test_details(self):
#         # Issue a GET request.
#         response = self.client.get('/')

#         # Check that the response is 200 OK.
#         self.assertEqual(response.status_code, 200)


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


class TestUrlIndex(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class TestUrlLogin(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)


class TestUrlLogout(SimpleTestCase, TestCase):
    def setUp(self):
        self.client = Client()

    def test_logout(self):
        response = self.client.get('/logout/', follow=True)
        # print(response.redirect_chain[0])  # Looks like ('/', 302)
        # excpected_url, status_code = response.redirect_chain[0]  # récupère l'adresse et le code de la redirection
        ''' print()
            print()
            print(response.redirect_chain[0])
            print()
            print() '''

        self.assertRedirects(response, expected_url='/', status_code=302, target_status_code=200)


class TestUrlSignUp(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sign_up(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)


class TestUrlPassword(SimpleTestCase, TestCase):
    def setUp(self):
        self.client = Client()

    def test_password(self):
        response = self.client.get('/password/', follow=True)
        print()
        print()
        print(response.redirect_chain[0])
        print()
        print()
        self.assertRedirects(response, expected_url='/login/?next=/password/', status_code=302, target_status_code=200)


class TestUrlBattle(SimpleTestCase, TestCase):
    def setUp(self):
        self.client = Client()

    def test_battle(self):
        response = self.client.get('/battle/', follow=True)
        '''print()
        print()
        print(response.redirect_chain[0])
        print()
        print()'''
        self.assertRedirects(response, expected_url='/login/?next=/battle/', status_code=302, target_status_code=200)


class TestUrlBattleWithSinglePlayerPk(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='bob', email='bob@bibi.com', password='bobbibi', pk=1)

    def test_battle_with_single_player_pk(self):
        response = self.client.get('battle/1/', self.user, follow=True)
        '''print()
        print()
        print(response.redirect_chain)
        print()
        print()'''
        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, expected_url='/battle/'+str(self.user.pk)+'/', status_code=302, target_status_code=200)


class TestUrlTestCPU(SimpleTestCase, TestCase):
    def setUp(self):
        self.client = Client()

    def test_testCPU(self):
        response = self.client.get('/testcpu/', follow=True)
        ''' print()
            print()
            print(response.redirect_chain[0])
            print()
            print() '''
        self.assertRedirects(response, expected_url='/login/?next=/testcpu/', status_code=302, target_status_code=200)


class TestUrlVersus(SimpleTestCase, TestCase):
    def setUp(self):
        self.client = Client()

    def test_versus(self):
        response = self.client.get('/versus/', follow=True)
        print()
        print()
        print(response.redirect_chain[0])
        print()
        print()
        self.assertRedirects(response, expected_url='/login/?next=/versus/', status_code=302, target_status_code=200)
