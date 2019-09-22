import unittest
from django.urls import reverse
from rest_framework import status


from commons.tests import APITestBaseCase
from commons.constants import EMPTY_FIELD_ERROR_TEXT, TEXT_WITH_210_CHARACTERS,\
    EMPTY_FIELD_REQUIRED_TEXT, get_maximum_error_text_in_field
from distributions.models import Distribution


@unittest.skip("skip for using views class")
class DistributionTest(APITestBaseCase):
    '''
    Tests belong to distribution functionality
    '''

    def setUp(self):
        '''
        urls and data initialization for testing
        '''
        self.url_list = 'distribution-list'
        self.url_detail = 'distribution-detail'
        data = {
            "name": "first distribution",
            "link_id": "TK2C5N53L/BKDQP7F4Y/ZZRtgDmYqAX5r5155AkzYQ0W",
            "is_active": True
        }
        self.distribution_id = self.create_distribution_for_principal_user(
            data)
        super(DistributionTest, self).setUp()

    def tearDown(self):
        """
        Remove and clean test data
        """
        Distribution.objects.all().delete()
        super(DistributionTest, self).tearDown()

    def test_same_user_see_distribution_list(self):
        '''
        test with the main purpose that the user can see only own distributions
        '''
        self.login_principal_user()
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertEqual(len(elements), 1)

    def test_same_user_create_distribution(self):
        '''
        test with the main purpose that the user can create a distribution
        '''
        self.login_principal_user()
        data = {
            "name": "other distribution",
            "link_id": "link"
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Distribution.objects.count(), 2)

    def test_same_user_create_empty_distribution(self):
        '''
        test with the main purpose to warn when distribution is created with an
        empty name
        '''
        self.login_principal_user()
        data = {
            "name": ""
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertIn(EMPTY_FIELD_ERROR_TEXT, elements['name'])
        self.assertIn(EMPTY_FIELD_REQUIRED_TEXT, elements['link_id'])
        self.assertEqual(Distribution.objects.count(), 1)

    def test_same_user_create_distribution_maximum_characters(self):
        '''
        test with the main purpose to warn when distribution is created with an name
        with more than the maximum characters
        '''
        self.login_principal_user()
        data = {
            "name": TEXT_WITH_210_CHARACTERS
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertIn(get_maximum_error_text_in_field(200), elements['name'])
        self.assertIn(EMPTY_FIELD_REQUIRED_TEXT, elements['link_id'])
        self.assertEqual(Distribution.objects.count(), 1)

    def test_same_user_edit_distribution(self):
        '''
        test with the main purpose that the user can edit a distribution
        '''
        self.login_principal_user()
        old_distribution = Distribution.objects.first()
        data = {
            "name": "other distribution",
            "link_id": "one link"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.distribution_id}),
            data
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Distribution.objects.count(), 1)
        new_distribution = Distribution.objects.first()
        self.assertEqual(new_distribution.name, data['name'])
        self.assertNotEqual(old_distribution.name, new_distribution.name)

    def test_same_user_edit_empty_distribution(self):
        '''
        test with the main purpose to warn when distribution is edit with an empty name
        '''
        self.login_principal_user()
        old_distribution = Distribution.objects.first()
        data = {
            "name": ""
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.distribution_id}),
            data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Distribution.objects.count(), 1)
        self.assertIn(
            EMPTY_FIELD_ERROR_TEXT,
            elements['name']
        )
        new_distribution = Distribution.objects.first()
        self.assertNotEqual(new_distribution.name, data['name'])
        self.assertEqual(old_distribution.name, new_distribution.name)

    def test_same_user_edit_distribution_maximum_characters(self):
        '''
        test with the main purpose to warn when distribution is edit with an name
        with more than the maximum characters
        '''
        self.login_principal_user()
        old_distribution = Distribution.objects.first()
        data = {
            "name": TEXT_WITH_210_CHARACTERS
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.distribution_id}),
            data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Distribution.objects.count(), 1)
        self.assertIn(
            get_maximum_error_text_in_field(200),
            elements['name']
        )
        new_distribution = Distribution.objects.first()
        self.assertNotEqual(new_distribution.name, data['name'])
        self.assertEqual(old_distribution.name, new_distribution.name)

    def test_same_user_delete_distribution(self):
        '''
        test with the main purpose that the user can delete a distribution
        '''
        self.login_principal_user()
        data = {
            "name": "other distribution"
        }
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.distribution_id}),
            data
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Distribution.objects.count(), 0)

    def test_other_user_see_distribution_list(self):
        '''
        test with the main purpose that the user can see only own distributions and no
        the other user's distributions
        '''
        self.login_secondary_user()
        response = self.client.get(reverse(self.url_list), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertEqual(len(elements), 0)

    def test_other_user_see_detail_distribution(self):
        '''
        test with the main purpose that the user can see only own distributions detail
        and not the others user's distributions detail
        '''
        self.login_secondary_user()
        data = {
            "name": "other name"
        }
        response = self.client.get(
            reverse(self.url_detail, kwargs={'pk': self.distribution_id}),
            data
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_other_user_edit_distribution(self):
        '''
        test with the main purpose that the user can edit only own distributions detail
        and not the others user's distributions detail
        '''
        self.login_secondary_user()
        old_distribution = Distribution.objects.first()
        data = {
            "name": "other name"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.distribution_id}),
            data
        )
        after_distribution = Distribution.objects.first()
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(old_distribution.name, after_distribution.name)
        self.assertEqual(Distribution.objects.count(), 1)

    def test_other_user_delete_distribution(self):
        '''
        test with the main purpose that the user can delete only own distributions
        and not the others user's distributions
        '''
        self.login_secondary_user()
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.distribution_id})
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(Distribution.objects.count(), 1)

    def test_unauthorized_user_see_distribution_list(self):
        '''
        test with the main purpose that the anonymous user can't see distributions
        '''
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_unauthorized_user_create_distribution(self):
        '''
        test with the main purpose that the anonymous user can't create
        distributions
        '''
        data = {
            "name": "unauthorized user distribution"
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(Distribution.objects.count(), 1)

    def test_unauthorized_user_detail_distribution(self):
        '''
        test with the main purpose that the anonymous user can't see distribution's
        detail
        '''
        data = {
            "name": "other name"
        }
        response = self.client.get(
            reverse(self.url_detail, kwargs={'pk': self.distribution_id}),
            data
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_unauthorized_user_edit_distribution(self):
        '''
        test with the main purpose that the anonymous user can't edit distribution's
        detail
        '''
        old_distribution = Distribution.objects.first()
        data = {
            "name": "other name"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.distribution_id}),
            data
        )
        after_distribution = Distribution.objects.first()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(old_distribution.name, after_distribution.name)
        self.assertEqual(Distribution.objects.count(), 1)

    def test_unauthorized_user_delete_distribution(self):
        '''
        test with the main purpose that the anonymous user can't delete distribution's
        detail
        '''
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.distribution_id})
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.assertEqual(Distribution.objects.count(), 1)
