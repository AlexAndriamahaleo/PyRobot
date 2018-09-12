from unittest import TestCase
from django.test import Client, SimpleTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import *
from .funct.funct import *
from .game.Game import Game
from .forms import *

# Create your tests here.


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


def init_user(**data_user):
    """
    Fonction qui crée et initialise un User et le renvoie.
    Contient :
        - l'id du User
        - son nom d'utilisateur
        - son email
        - son mot de passe
    :param int or str data_user:
    :return: return the User created
    """
    user = User(username=data_user['username'], email=data_user['email'], password=data_user['password'])
    user.id = data_user['id']
    user.save()
    return user


def init_user_profile(**data_user):
    """
    Fonction qui permet de créer et initialiser un UserProfile à partir d'un user, et le renvoie.
    Contient :
        - l'id du User
        - son nom d'utilisateur
        - son email
        - son mot de passe
    :param int or str data_user:
    :return: Return the UserProfile created
    """
    user = init_user(**data_user)
    user_profile = UserProfile(user=user)
    user_profile.id = data_user['id']
    user_profile.save()
    return user_profile


def init_tank(user_profile):
    i = Ia(owner=user_profile, name='Script de {}'.format(user_profile.user.username.capitalize()), active=True)
    i.save()
    w = Weapon(name='Canon', price=100, attackValue=100, range=10, attackCost=10, pathIcon='canon_1.png')
    w.save()
    a = Armor(name='Blindage', price=100, armorValue=100, pathIcon='shield_1.png')
    a.save()
    c = Caterpillar(name='Chenille', price=100, moveValue=4, pathIcon='cater_1.png')
    c.save()
    n = NavSystem(name='Processeur', price=100, actionValue=100, pathIcon='circuit_1.png')
    n.save()
    tank = Tank(owner=user_profile, ia=i, weapon=w, armor=a, caterpillar=c, navSystem=n)
    tank.save()
    return tank


class TestUrls(SimpleTestCase, TestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        response = self.client.get(reverse('backend:index'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse('backend:login'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        # Set follow=True to get the attribute redirect_chain
        response = self.client.get(reverse('backend:logout'), follow=True)
        # self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, expected_url=reverse('backend:index'), status_code=302, target_status_code=200)

    def test_sign_up(self):
        response = self.client.get(reverse('backend:signUp2'))
        self.assertEqual(response.status_code, 200)

    def test_password(self):
        response = self.client.get(reverse('backend:change_password'), follow=True)
        self.assertRedirects(response, expected_url='/login/?next=/password/', status_code=302, target_status_code=200)

    def test_battle(self):
        response = self.client.get(reverse('backend:fight'), follow=True)
        SimpleTestCase().assertRedirects(response, expected_url='/login/?next=/battle/', status_code=302,
                                         target_status_code=200)
    """
    def test_battle_championship(self):
        self.user1 = init_user_profile(id=1, username='bob', email='bob@bibi.com', password='bobbibi')
        self.user2 = init_user_profile(id=2, username='marc', email='marc@mi.com', password='marcima')

        self.tank1 = init_tank(self.user1)
        self.tank2 = init_tank(self.user2)

        self.champ = Championship(name='ch')
        self.champ.id = 1
        self.champ.save()
        self.champ.add_user(self.user1)
        self.champ.add_user(self.user2)
        self.champ.save()
        # print("\n\n{}\n{}\n\n".format(UserProfile.objects.all(), Championship.objects.all()))
        # print('test = ', self.champ.pk)

        game = Game(self.tank1, self.tank2, self.user1.get_active_ai_script(), self.user2.get_active_ai_script(), self.champ)
        game.run(0)

        # response = self.client.get(reverse('backend:fight'), player_pk=self.user2.pk, follow=True)
        # response = self.client.get('battle/2/', player_pk=self.user2.pk, follow=True)
        # print("\n\n{}\n\n".format(response))
        # self.assertEqual(response.status_code, 200)
        # SimpleTestCase.assertRedirects(response, expected_url='/battle/'+str(self.user.pk)+'/',
        #                                status_code=302, target_status_code=200)
    """
    def test_testCPU(self):
        response = self.client.get(reverse('backend:testcpu'), follow=True)
        self.assertRedirects(response, expected_url='/login/?next=/testcpu/', status_code=302, target_status_code=200)

    def test_versus(self):
        response = self.client.get(reverse('backend:versus', args=[0]), follow=True)
        self.assertRedirects(response, expected_url='/login/?next=/versus/0/', status_code=302, target_status_code=200)

    def test_replay(self):
        response = self.client.get(reverse('backend:replay'), follow=True)
        self.assertRedirects(response, expected_url='/login/?next=/replay/', status_code=302, target_status_code=200)

    def test_editor(self):
        response = self.client.get(reverse('backend:editor'), follow=True)
        self.assertRedirects(response, expected_url='/login/?next=/editor/', status_code=302, target_status_code=200)
    """
    def test_editor_detail(self):
        response = self.client.get(reverse('backend:editorDetail'), follow=True)
        self.assertRedirects(response, expected_url='/login/?next=/editor/1/', status_code=302, target_status_code=200)
    """
    def test_help(self):
        response = self.client.get(reverse('backend:help'), follow=True)
        self.assertRedirects(response, expected_url='/login/?next=/help/', status_code=302, target_status_code=200)

    def test_documentation(self):
        response = self.client.get(reverse('backend:documentation'), follow=True)
        self.assertRedirects(response, expected_url='/login/?next=/documentation/', status_code=302,
                             target_status_code=200)

    def test_faq(self):
        pass
        # response = self.client.get(reverse('backend:faq'))
        # self.assertEqual(response.status_code, 200)

    def test_tutoriel(self):
        response = self.client.get(reverse('backend:tutoriels'), follow=True)
        self.assertRedirects(response, expected_url='/login/?next=/tutoriels/', status_code=302, target_status_code=200)

    def test_battle_histories(self):
        response = self.client.get(reverse('backend:battle_histories'), follow=True)
        self.assertRedirects(response, expected_url='/login/?next=/battle-histories/', status_code=302,
                             target_status_code=200)

    def test_finish_battle(self):
        response = self.client.get(reverse('backend:finish_battle'), follow=True)
        # print("\n\n{}\n\n".format(response.redirect_chain[0]))
        self.assertRedirects(response, expected_url='/login/?next=/finish-battle/', status_code=302,
                             target_status_code=200)
