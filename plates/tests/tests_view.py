from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from commons.tests import UserLoginMixin
from commons.constants import EMPTY_FIELD_REQUIRED_TEXT_ES
from meals.models import Meal
from plates.models import Plate
from plates.forms import PlateModelForm


class TestplateCreate(TestCase, UserLoginMixin):

    def setUp(self):
        self.url = reverse('plate-create')
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()

    def tearDown(self):
        self.client.logout()
        Plate.objects.all().delete()
        Meal.objects.all().delete()
        self.delete_all_user()

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertIsInstance(response.context_data['form'], PlateModelForm)

    def test_form_errors(self):
        self.assertEqual(Plate.objects.all().count(), 0)
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertEqual(len(response.context_data['form'].errors.keys()), 1)
        self.assertFormError(response, 'form', 'name', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertEqual(Plate.objects.all().count(), 0)

    def test_create_successful(self):
        self.assertEqual(Plate.objects.all().count(), 0)
        data = {
            'name': 'Vegetariano'
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('object_list', response.context_data)
        self.assertEqual(len(response.context_data['object_list']), 1)
        self.assertEqual(response.context_data['object_list'][0].name, data['name'])
        self.assertEqual(Plate.objects.all().count(), 1)

    def test_create_successful_with_meals(self):
        self.assertEqual(Plate.objects.all().count(), 0)
        meal_1 = Meal.objects.create(name="meal 1", owner=self.nora)
        meal_2 = Meal.objects.create(name="meal 2", owner=self.nora)
        data = {
            'name': 'Vegetariano',
            'meals': [meal_1.id, meal_2.id]
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('object_list', response.context_data)
        self.assertEqual(len(response.context_data['object_list']), 1)
        self.assertEqual(response.context_data['object_list'][0].name, data['name'])
        self.assertEqual(Plate.objects.all().count(), 1)


class TestplateUpdate(TestCase, UserLoginMixin):

    def setUp(self):
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()
        self.plate = Plate.objects.create(owner=self.nora, name="test")
        self.url = reverse('plate-update', kwargs={'pk': self.plate.id})

    def tearDown(self):
        self.client.logout()
        Plate.objects.all().delete()
        self.delete_all_user()

    def test_get_form(self):
        self.assertEqual(Plate.objects.all().count(), 1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertIsInstance(response.context_data['form'], PlateModelForm)
        self.assertEqual(Plate.objects.all().count(), 1)

    def test_form_errors(self):
        self.assertEqual(Plate.objects.all().count(), 1)
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertEqual(len(response.context_data['form'].errors.keys()), 1)
        self.assertFormError(response, 'form', 'name', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertEqual(Plate.objects.all().count(), 1)

    def test_update_successful(self):
        self.assertEqual(Plate.objects.all().count(), 1)
        meal_1 = Meal.objects.create(name="meal 1", owner=self.nora)
        meal_2 = Meal.objects.create(name="meal 2", owner=self.nora)
        data = {
            'name': 'Vegetariano',
            'meals': [meal_1.id, meal_2.id]
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('object_list', response.context_data)
        self.assertEqual(len(response.context_data['object_list']), 1)
        self.assertEqual(response.context_data['object_list'][0].name, data['name'])
        self.assertEqual(response.context_data['object_list'][0].meals.all().count(), len(data['meals']))
        meals_name = response.context_data['object_list'][0].meals.all().values_list('id', flat=True)
        self.assertIn(data['meals'][0], meals_name)
        plate = Plate.objects.get(id=self.plate.id)
        self.assertEqual(plate.name, data['name'])
        self.assertEqual(Plate.objects.all().count(), 1)


class TestplateDelete(TestCase, UserLoginMixin):

    def setUp(self):
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()
        self.plate = Plate.objects.create(owner=self.nora, name="test")
        self.url = reverse('plate-delete', kwargs={'pk': self.plate.id})

    def tearDown(self):
        self.client.logout()
        Plate.objects.all().delete()
        self.delete_all_user()

    def test_successful_deletion(self):
        self.assertEqual(Plate.objects.all().count(), 1)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, "%s" % (reverse('plate-list')))
        self.assertEqual(Plate.objects.all().count(), 0)


class TestplateOtherUser(TestCase, UserLoginMixin):
    def setUp(self):
        self.url = reverse('plate-create')
        self.other_nora = self.create_user(username='other nora', is_staff=True)
        self.nora = self.create_user(username='nora', is_staff=True)
        self.plate = Plate.objects.create(owner=self.other_nora, name="test")
        self.url = reverse('plate-update', kwargs={'pk': self.plate.id})
        self.setup_logged_in_client()

    def tearDown(self):
        self.client.logout()
        Plate.objects.all().delete()
        self.delete_all_user()

    def test_update_successful(self):
        self.assertEqual(Plate.objects.all().count(), 1)
        data = {
            'name': 'Vegetariano'
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestplateAnonymous(TestCase):

    def setUp(self):
        self.url = reverse('plate-create')

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
