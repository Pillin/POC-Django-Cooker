

from django.urls import reverse
from django.test.client import Client
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from tags.models import Tag
from meals.models import Meal
from users.models import User
from menus.models import Menu
from plates.models import Plate
from distributions.models import Distribution


class APITestBaseCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        '''
        '''
        super(APITestBaseCase, cls).setUpClass()
        cls.client = APIClient()
        cls.user = mommy.make(
            'users.User',
            username='nora',
            password='nora1234',
            email="nora@gmail.com",
            is_staff=True,
            is_active=True,
            is_superuser=True
        )

        cls.other_user = mommy.make(
            'users.User',
            username="la_otra_nora",
            password="nora1234",
            email="la_otra_nora@test.cl",
            is_staff=True,
            is_active=True,
            is_superuser=True
        )

    @classmethod
    def tearDownClass(cls):
        '''
        '''
        cls.user.delete()
        cls.other_user.delete()
        super(APITestBaseCase, cls).tearDownClass()

    def tearDown(self):
        """
        Remove and clean test data
        """
        self.client.logout()
        super(APITestBaseCase, self).tearDown()

    def test_login(self):
        '''
        '''
        url = reverse('rest_framework:login')
        data = {
            'username': 'nora',
            'password': 'nora1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(200, response.status_code)

    def login(self, username, password):
        '''
        '''
        data = {
            'username': username,
            'password': password
        }
        self.client.login(**data)
        user = User.objects.get(username=username)
        self.client.force_authenticate(user=user)

    def login_principal_user(self):
        '''
        '''
        self.login("nora", "nora1234")
        self.assertTrue(self.user.is_authenticated)

    def login_secondary_user(self):
        '''
        '''
        self.login("la_otra_nora", "nora1234")
        self.assertTrue(self.user.is_authenticated)

    def logout(self):
        '''
        '''
        self.client.logout()

    def create_object(self, Model, url, data):
        '''
        create tag for any user
        '''
        response = self.client.post(reverse(url), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        object_id = response.json()['id']
        self.assertEqual(Model.objects.filter(id=object_id).count(), 1)
        return object_id

    def create_tag_for_principal_user(self, name):
        '''
        create tag for the principal user
        '''
        self.login_principal_user()
        tag_id = self.create_object(Tag, 'tag-list', {"name": name})
        self.logout()
        return tag_id

    def create_meal_for_principal_user(self, data):
        '''
        create tag for the principal user
        '''
        self.login_principal_user()
        meal_id = self.create_object(Meal, 'meal-list', data)
        self.logout()
        return meal_id

    def create_menu_for_principal_user(self, data):
        self.login_principal_user()
        menu_id = self.create_object(Menu, 'menu-list', data)
        self.logout()
        return menu_id

    def create_plate_for_principal_user(self, data):
        self.login_principal_user()
        plate_id = self.create_object(Plate, 'plate-list', data)
        self.logout()
        return plate_id

    def create_distribution_for_principal_user(self, data):
        self.login_principal_user()
        distribution_id = self.create_object(
            Distribution, 'distribution-list', data)
        self.logout()
        return distribution_id


class UserLoginMixin:
    password = 'password'
    user_permissions = []
    user = None

    def create_user(self, username, is_staff=False):
        self.user = User.objects.create_user(
            username=username,
            password=self.password
        )
        self.username = username
        self.user.is_active = True
        self.user.is_staff = is_staff
        self.user.save()
        return self.user

    def delete_user(self):
        self.user.delete()

    def delete_all_user(self):
        User.objects.all().delete()

    def login_user(self):
        self.client.login(
            username=self.username,
            password=self.password
        )

    def setup_logged_in_client(self):
        self.client = Client()
        self.login_user()


class CSRFMixin:
    def get_form_token(self, url):
        self.client.get(url, follow=True)
        return self.client.cookies['csrftoken'].value
