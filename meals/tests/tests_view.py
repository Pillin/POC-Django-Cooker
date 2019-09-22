from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from commons.tests import UserLoginMixin
from commons.constants import EMPTY_FIELD_REQUIRED_TEXT_ES
from tags.models import Tag
from meals.models import Meal
from meals.forms import MealModelForm


class TestMealCreate(TestCase, UserLoginMixin):

    def setUp(self):
        self.url = reverse('meal-create')
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()

    def tearDown(self):
        self.client.logout()
        Meal.objects.all().delete()
        Tag.objects.all().delete()
        self.delete_all_user()

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertIsInstance(response.context_data['form'], MealModelForm)

    def test_form_errors(self):
        self.assertEqual(Meal.objects.all().count(), 0)
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertEqual(len(response.context_data['form'].errors.keys()), 1)
        self.assertFormError(response, 'form', 'name', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertEqual(Meal.objects.all().count(), 0)

    def test_create_successful(self):
        self.assertEqual(Meal.objects.all().count(), 0)
        data = {
            'name': 'Vegetariano'
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('object_list', response.context_data)
        self.assertEqual(len(response.context_data['object_list']), 1)
        self.assertEqual(response.context_data['object_list'][0].name, data['name'])
        self.assertEqual(Meal.objects.all().count(), 1)

    def test_create_successful_with_tags(self):
        self.assertEqual(Meal.objects.all().count(), 0)
        tag_1 = Tag.objects.create(name="tag 1", owner=self.nora)
        tag_2 = Tag.objects.create(name="tag 2", owner=self.nora)
        data = {
            'name': 'Vegetariano',
            'tags': [tag_1.id, tag_2.id]
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('object_list', response.context_data)
        self.assertEqual(len(response.context_data['object_list']), 1)
        self.assertEqual(response.context_data['object_list'][0].name, data['name'])
        self.assertEqual(Meal.objects.all().count(), 1)


class TestMealUpdate(TestCase, UserLoginMixin):

    def setUp(self):
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()
        self.meal = Meal.objects.create(owner=self.nora, name="test")
        self.url = reverse('meal-update', kwargs={'pk': self.meal.id})

    def tearDown(self):
        self.client.logout()
        Meal.objects.all().delete()
        self.delete_all_user()

    def test_get_form(self):
        self.assertEqual(Meal.objects.all().count(), 1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertIsInstance(response.context_data['form'], MealModelForm)
        self.assertEqual(Meal.objects.all().count(), 1)

    def test_form_errors(self):
        self.assertEqual(Meal.objects.all().count(), 1)
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertEqual(len(response.context_data['form'].errors.keys()), 1)
        self.assertFormError(response, 'form', 'name', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertEqual(Meal.objects.all().count(), 1)

    def test_update_successful(self):
        self.assertEqual(Meal.objects.all().count(), 1)
        tag_1 = Tag.objects.create(name="tag 1", owner=self.nora)
        tag_2 = Tag.objects.create(name="tag 2", owner=self.nora)
        data = {
            'name': 'Vegetariano',
            'tags': [tag_1.id, tag_2.id]
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('object_list', response.context_data)
        self.assertEqual(len(response.context_data['object_list']), 1)
        self.assertEqual(response.context_data['object_list'][0].name, data['name'])
        self.assertEqual(response.context_data['object_list'][0].tags.all().count(), len(data['tags']))
        tags_name = response.context_data['object_list'][0].tags.all().values_list('id', flat=True)
        self.assertIn(data['tags'][0], tags_name)
        meal = Meal.objects.get(id=self.meal.id)
        self.assertEqual(meal.name, data['name'])
        self.assertEqual(Meal.objects.all().count(), 1)


class TestMealDelete(TestCase, UserLoginMixin):

    def setUp(self):
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()
        self.meal = Meal.objects.create(owner=self.nora, name="test")
        self.url = reverse('meal-delete', kwargs={'pk': self.meal.id})

    def tearDown(self):
        self.client.logout()
        Meal.objects.all().delete()
        self.delete_all_user()

    def test_successful_deletion(self):
        self.assertEqual(Meal.objects.all().count(), 1)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, "%s" % (reverse('meal-list')))
        self.assertEqual(Meal.objects.all().count(), 0)


class TestMealOtherUser(TestCase, UserLoginMixin):
    def setUp(self):
        self.url = reverse('meal-create')
        self.other_nora = self.create_user(username='other nora', is_staff=True)
        self.nora = self.create_user(username='nora', is_staff=True)
        self.meal = Meal.objects.create(owner=self.other_nora, name="test")
        self.url = reverse('meal-update', kwargs={'pk': self.meal.id})
        self.setup_logged_in_client()

    def tearDown(self):
        self.client.logout()
        Meal.objects.all().delete()
        self.delete_all_user()

    def test_update_successful(self):
        self.assertEqual(Meal.objects.all().count(), 1)
        data = {
            'name': 'Vegetariano'
        }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestMealAnonymous(TestCase):

    def setUp(self):
        self.url = reverse('meal-create')

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
