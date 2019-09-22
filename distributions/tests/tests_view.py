from datetime import time
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from commons.tests import UserLoginMixin
from commons.constants import EMPTY_FIELD_REQUIRED_TEXT_ES
from distributions.models import Distribution
from distributions.forms import DistributionModelForm


class TestdistributionCreate(TestCase, UserLoginMixin):

    def setUp(self):
        self.url = reverse('distribution-create')
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()

    def tearDown(self):
        self.client.logout()
        Distribution.objects.all().delete()
        self.delete_all_user()

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertIsInstance(response.context_data['form'], DistributionModelForm)

    def test_form_errors(self):
        self.assertEqual(Distribution.objects.all().count(), 0)
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertEqual(len(response.context_data['form'].errors.keys()), 4)
        self.assertFormError(response, 'form', 'name', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertFormError(response, 'form', 'link_id', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertFormError(response, 'form', 'distribution_hour_link', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertFormError(response, 'form', 'end_available_distribution_link', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertEqual(Distribution.objects.all().count(), 0)

    def test_create_successful(self):
        self.assertEqual(Distribution.objects.all().count(), 0)
        data = {
            'name': 'Vegetariano',
            'link_id': 'link_id',
            'distribution_hour_link': time(),
            'end_available_distribution_link': time()
        }

        response = self.client.post(self.url, data=data, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Distribution.objects.all().count(), 1)


class TestdistributionUpdate(TestCase, UserLoginMixin):

    def setUp(self):
        self.nora = self.create_user(username='nora', is_staff=True)
        self.setup_logged_in_client()
        self.distribution = Distribution.objects.create(
            owner=self.nora,
            name="test",
            is_active=True,
            distribution_hour_link=time(),
            end_available_distribution_link=time()
        )
        self.url = reverse('distribution-update', kwargs={'pk': self.distribution.id})

    def tearDown(self):
        self.client.logout()
        Distribution.objects.all().delete()
        self.delete_all_user()

    def test_get_form(self):
        self.assertEqual(Distribution.objects.all().count(), 1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertIsInstance(response.context_data['form'], DistributionModelForm)
        self.assertEqual(Distribution.objects.all().count(), 1)

    def test_form_errors(self):
        self.assertEqual(Distribution.objects.all().count(), 1)
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIn('titlename', response.context_data)
        self.assertEqual(len(response.context_data['form'].errors.keys()), 4)
        self.assertFormError(response, 'form', 'name', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertFormError(response, 'form', 'distribution_hour_link', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertFormError(response, 'form', 'end_available_distribution_link', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertFormError(response, 'form', 'link_id', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertEqual(Distribution.objects.all().count(), 1)

    def test_update_successful(self):
        self.assertEqual(Distribution.objects.all().count(), 1)
        data = {
            'name': 'Vegetariano',
            'link_id': 'link_id',
            'distribution_hour_link': time(),
            'end_available_distribution_link': time()
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        distribution = Distribution.objects.get(id=self.distribution.id)
        self.assertEqual(distribution.name, data['name'])
        self.assertEqual(Distribution.objects.all().count(), 1)


class TestdistributionOtherUser(TestCase, UserLoginMixin):
    def setUp(self):
        self.url = reverse('distribution-create')
        self.other_nora = self.create_user(username='other nora', is_staff=True)
        self.nora = self.create_user(username='nora', is_staff=True)
        self.distribution = Distribution.objects.create(
            owner=self.other_nora,
            name="test",
            is_active=True,
            distribution_hour_link=time(),
            end_available_distribution_link=time()
        )
        self.url = reverse('distribution-update', kwargs={'pk': self.distribution.id})
        self.setup_logged_in_client()

    def tearDown(self):
        self.client.logout()
        Distribution.objects.all().delete()
        self.delete_all_user()

    def test_update_successful(self):
        self.assertEqual(Distribution.objects.all().count(), 1)
        data = {
            'name': 'Vegetariano'
        }

        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestdistributionAnonymous(TestCase):

    def setUp(self):
        self.url = reverse('distribution-create')

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        