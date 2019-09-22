from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from commons.tests import UserLoginMixin
from commons.constants import EMPTY_FIELD_REQUIRED_TEXT_ES
from tags.models import Tag
from tags.forms import TagModelForm


class TestTagCreate(TestCase, UserLoginMixin):

    def setUp(self):
        self.url = reverse('tag-create')
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()

    def tearDown(self):
        self.client.logout()
        Tag.objects.all().delete()
        self.delete_all_user()

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertIsInstance(response.context_data['form'], TagModelForm)

    def test_form_errors(self):
        self.assertEqual(Tag.objects.all().count(), 0)
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertEqual(len(response.context_data['form'].errors.keys()), 1)
        self.assertFormError(response, 'form', 'name', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertEqual(Tag.objects.all().count(), 0)

    def test_create_successful(self):
        self.assertEqual(Tag.objects.all().count(), 0)
        data = {
            'name': 'Vegetariano'
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('object_list', response.context_data)
        self.assertEqual(len(response.context_data['object_list']), 1)
        self.assertEqual(response.context_data['object_list'][0].name, data['name'])
        self.assertEqual(Tag.objects.all().count(), 1)


class TestTagUpdate(TestCase, UserLoginMixin):

    def setUp(self):
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()
        self.tag = Tag.objects.create(owner=self.nora, name="test")
        self.url = reverse('tag-update', kwargs={'pk': self.tag.id})

    def tearDown(self):
        self.client.logout()
        Tag.objects.all().delete()
        self.delete_all_user()

    def test_get_form(self):
        self.assertEqual(Tag.objects.all().count(), 1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertIsInstance(response.context_data['form'], TagModelForm)
        self.assertEqual(Tag.objects.all().count(), 1)

    def test_form_errors(self):
        self.assertEqual(Tag.objects.all().count(), 1)
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertEqual(len(response.context_data['form'].errors.keys()), 1)
        self.assertFormError(response, 'form', 'name', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertEqual(Tag.objects.all().count(), 1)

    def test_update_successful(self):
        self.assertEqual(Tag.objects.all().count(), 1)
        data = {
            'name': 'Vegetariano'
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('object_list', response.context_data)
        self.assertEqual(len(response.context_data['object_list']), 1)
        self.assertEqual(response.context_data['object_list'][0].name, data['name'])
        tag = Tag.objects.get(id=self.tag.id)
        self.assertEqual(tag.name, data['name'])
        self.assertEqual(Tag.objects.all().count(), 1)


class TestTagDelete(TestCase, UserLoginMixin):

    def setUp(self):
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()
        self.tag = Tag.objects.create(owner=self.nora, name="test")
        self.url = reverse('tag-delete', kwargs={'pk': self.tag.id})

    def tearDown(self):
        self.client.logout()
        Tag.objects.all().delete()
        self.delete_all_user()

    def test_successful_deletion(self):
        self.assertEqual(Tag.objects.all().count(), 1)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, "%s" % (reverse('tag-list')))
        self.assertEqual(Tag.objects.all().count(), 0)


class TestTagOtherUser(TestCase, UserLoginMixin):
    def setUp(self):
        self.url = reverse('tag-create')
        self.other_nora = self.create_user(username='other nora', is_staff=True)
        self.nora = self.create_user(username='nora', is_staff=True)
        self.tag = Tag.objects.create(owner=self.other_nora, name="test")
        self.url = reverse('tag-update', kwargs={'pk': self.tag.id})
        self.setup_logged_in_client()

    def tearDown(self):
        self.client.logout()
        Tag.objects.all().delete()
        self.delete_all_user()

    def test_update_successful(self):
        self.assertEqual(Tag.objects.all().count(), 1)
        data = {
            'name': 'Vegetariano'
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestTagAnonymous(TestCase):

    def setUp(self):
        self.url = reverse('tag-create')

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
