from datetime import time, date
from django.test.utils import override_settings
from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from commons.tests import UserLoginMixin
from commons.constants import EMPTY_FIELD_REQUIRED_TEXT_ES
from commons.mocks import mock_call_send_link_task
from distributions.models import Distribution
from deliveries.models import Delivery
from deliveries.celery import call_send_link_task
from meals.models import Meal
from menus.models import Menu
from menus.forms import MenuModelForm
from plates.models import Plate


class TestMenuCreate(TestCase, UserLoginMixin):

    def setUp(self):
        self.url = reverse('menu-create')
        self.nora = self.create_user(username='nora', is_staff=True)
        self.distribution = Distribution.objects.create(
            name="test",
            link_id="link",
            is_active=True,
            distribution_hour_link=time(),
            end_available_distribution_link=time(),
            owner=self.nora,
        )
        self.setup_logged_in_client()

    def tearDown(self):
        self.client.logout()
        Menu.objects.all().delete()
        Plate.objects.all().delete()
        self.delete_all_user()

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertIsInstance(response.context_data['form'], MenuModelForm)

    def test_form_errors(self):
        self.assertEqual(Menu.objects.all().count(), 0)
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertEqual(len(response.context_data['form'].errors.keys()), 3)
        self.assertFormError(response, 'form', 'plates', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertFormError(response, 'form', 'date', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertFormError(response, 'form', 'name', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertEqual(Menu.objects.all().count(), 0)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_create_successful_with_plates(self):
        call_send_link_task.apply_async = mock_call_send_link_task
        self.assertEqual(Menu.objects.all().count(), 0)
        plate_1 = Plate.objects.create(name="plate 1", owner=self.nora)
        plate_2 = Plate.objects.create(name="plate 2", owner=self.nora)
        data = {
            'name': 'Vegetariano',
            'date': '15/11/2019',
            'plates': [plate_1.id, plate_2.id]
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('object_list', response.context_data)
        self.assertEqual(len(response.context_data['object_list']), 1)
        self.assertEqual(response.context_data['object_list'][0].name, data['name'])
        self.assertEqual(Menu.objects.all().count(), 1)


class TestMenuUpdate(TestCase, UserLoginMixin):

    def setUp(self):
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()
        self.distribution = Distribution.objects.create(
            name="test",
            link_id="link",
            is_active=True,
            distribution_hour_link=time(),
            end_available_distribution_link=time(),
            owner=self.nora,
        )
        self.menu = Menu.objects.create(
            owner=self.nora,
            name="test"
        )
        self.delivery = Delivery.objects.create(
            menu=self.menu,
            distribution=self.distribution,
            date=date.today(),
            owner=self.nora,
        )
        self.url = reverse('menu-update', kwargs={'pk': self.menu.id})

    def tearDown(self):
        self.client.logout()
        Menu.objects.all().delete()
        self.delete_all_user()

    def test_get_form(self):
        self.assertEqual(Menu.objects.all().count(), 1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertIsInstance(response.context_data['form'], MenuModelForm)
        self.assertEqual(Menu.objects.all().count(), 1)

    def test_form_errors(self):
        self.assertEqual(Menu.objects.all().count(), 1)
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertEqual(len(response.context_data['form'].errors.keys()), 3)
        self.assertFormError(response, 'form', 'plates', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertFormError(response, 'form', 'date', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertFormError(response, 'form', 'name', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertEqual(Menu.objects.all().count(), 1)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_update_successful(self):
        call_send_link_task.apply_async = mock_call_send_link_task
        self.assertEqual(Menu.objects.all().count(), 1)
        meal = Meal.objects.create(name="meal 1", owner=self.nora)
        plate_1 = Plate.objects.create(name="plate 1", owner=self.nora)
        plate_1.meals.add(meal)
        plate_2 = Plate.objects.create(name="plate 2", owner=self.nora)
        plate_2.meals.add(meal)
        data = {
            'name': 'Vegetariano',
            'date': '15/11/2019',
            'plates': [plate_1.id, plate_2.id]
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('object_list', response.context_data)
        self.assertEqual(len(response.context_data['object_list']), 1)
        self.assertEqual(response.context_data['object_list'][0].name, data['name'])
        self.assertEqual(response.context_data['object_list'][0].plates.all().count(), len(data['plates']))
        plates_name = response.context_data['object_list'][0].plates.all().values_list('id', flat=True)
        self.assertIn(data['plates'][0], plates_name)
        menu = Menu.objects.get(id=self.menu.id)
        self.assertEqual(menu.name, data['name'])
        self.assertEqual(Menu.objects.all().count(), 1)


class TestMenuDelete(TestCase, UserLoginMixin):

    def setUp(self):
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()
        self.menu = Menu.objects.create(owner=self.nora, name="test")
        self.url = reverse('menu-delete', kwargs={'pk': self.menu.id})

    def tearDown(self):
        self.client.logout()
        Menu.objects.all().delete()
        self.delete_all_user()

    def test_successful_deletion(self):
        self.assertEqual(Menu.objects.all().count(), 1)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, "%s" % (reverse('menu-list')))
        self.assertEqual(Menu.objects.all().count(), 0)


class TestMenuOtherUser(TestCase, UserLoginMixin):
    def setUp(self):
        self.url = reverse('menu-create')
        self.other_nora = self.create_user(username='other nora', is_staff=True)
        self.nora = self.create_user(username='nora', is_staff=True)
        self.menu = Menu.objects.create(owner=self.other_nora, name="test")
        self.url = reverse('menu-update', kwargs={'pk': self.menu.id})
        self.setup_logged_in_client()

    def tearDown(self):
        self.client.logout()
        Menu.objects.all().delete()
        self.delete_all_user()

    def test_update_successful(self):
        self.assertEqual(Menu.objects.all().count(), 1)
        meal = Meal.objects.create(name="meal 1", owner=self.nora)
        plate_1 = Plate.objects.create(name="plate 1", owner=self.nora)
        plate_1.meals.add(meal)
        plate_2 = Plate.objects.create(name="plate 2", owner=self.nora)
        plate_2.meals.add(meal)
        data = {
            'name': 'Vegetariano',
            'date': '15/11/2019',
            'plates': [plate_1.id, plate_2.id]
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestMenuAnonymous(TestCase):

    def setUp(self):
        self.url = reverse('menu-create')

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
