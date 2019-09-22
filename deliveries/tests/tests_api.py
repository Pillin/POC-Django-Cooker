import unittest
from datetime import date, timedelta
from django.urls import reverse
from rest_framework import status


from commons.tests import APITestBaseCase
from commons.constants import EMPTY_FIELD_ERROR_TEXT, TEXT_WITH_210_CHARACTERS,\
    get_maximum_error_text_in_field
from deliveries.models import Delivery


@unittest.skip("skip for using views class")
class deliveryTest(APITestBaseCase):
    '''
    Tests belong to delivery functionality
    '''

    def setUp(self):
        '''
        urls and data initialization for testing
        '''
        self.url_list = 'delivery-list'
        self.url_detail = 'delivery-detail'

        self.unique_meal_id = self.create_meal_for_principal_user(
            {"name": "first meal"})
        self.plate_id = self.create_plate_for_principal_user({
            "name": "first plate",
            "meals": [self.unique_meal_id]
        })
        self.menu_id = self.create_menu_for_principal_user({
            "name": "firt menu",
            "plates": [self.unique_plate_id]
        })
        self.distribution_id = self.create_distribution_for_principal_user({})
        data = {
            "distribution": self.distribution_id,
            "menu": self.menu_id,
            "date": date.today() + timedelta(days=1)
        }
        self.delivery_id = self.create_delivery_for_principal_user(data)
        super(deliveryTest, self).setUp()

    def tearDown(self):
        """
        Remove and clean test data
        """
        Delivery.objects.all().delete()
        super(deliveryTest, self).tearDown()

    def test_same_user_see_delivery_list(self):
        '''
        test with the main purpose that the user can see only own deliverys
        '''
        self.login_principal_user()
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertEqual(len(elements), 1)

    def test_same_user_create_delivery(self):
        '''
        test with the main purpose that the user can create a delivery
        '''
        self.login_principal_user()
        data = {
            "name": "other delivery"
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Delivery.objects.count(), 2)

    def test_same_user_create_empty_delivery(self):
        '''
        test with the main purpose to warn when delivery is created with an
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
        self.assertEqual(Delivery.objects.count(), 1)

    def test_same_user_create_delivery_maximum_characters(self):
        '''
        test with the main purpose to warn when delivery is created with an name
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
        self.assertEqual(Delivery.objects.count(), 1)

    def test_same_user_edit_delivery(self):
        '''
        test with the main purpose that the user can edit a delivery
        '''
        self.login_principal_user()
        old_delivery = Delivery.objects.first()
        data = {
            "name": "other delivery"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.delivery_id}),
            data
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Delivery.objects.count(), 1)
        new_delivery = Delivery.objects.first()
        self.assertEqual(new_delivery.name, data['name'])
        self.assertNotEqual(old_delivery.name, new_delivery.name)

    def test_same_user_edit_empty_delivery(self):
        '''
        test with the main purpose to warn when delivery is edit with an empty name
        '''
        self.login_principal_user()
        old_delivery = Delivery.objects.first()
        data = {
            "name": ""
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.delivery_id}),
            data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Delivery.objects.count(), 1)
        self.assertIn(
            EMPTY_FIELD_ERROR_TEXT,
            elements['name']
        )
        new_delivery = Delivery.objects.first()
        self.assertNotEqual(new_delivery.name, data['name'])
        self.assertEqual(old_delivery.name, new_delivery.name)

    def test_same_user_edit_delivery_maximum_characters(self):
        '''
        test with the main purpose to warn when delivery is edit with an name
        with more than the maximum characters
        '''
        self.login_principal_user()
        old_delivery = Delivery.objects.first()
        data = {
            "name": TEXT_WITH_210_CHARACTERS
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.delivery_id}),
            data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Delivery.objects.count(), 1)
        self.assertIn(
            get_maximum_error_text_in_field(200),
            elements['name']
        )
        new_delivery = Delivery.objects.first()
        self.assertNotEqual(new_delivery.name, data['name'])
        self.assertEqual(old_delivery.name, new_delivery.name)

    def test_same_user_delete_delivery(self):
        '''
        test with the main purpose that the user can delete a delivery
        '''
        self.login_principal_user()
        data = {
            "name": "other delivery"
        }
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.delivery_id}),
            data
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Delivery.objects.count(), 0)

    def test_other_user_see_delivery_list(self):
        '''
        test with the main purpose that the user can see only own deliverys and no
        the other user's deliverys
        '''
        self.login_secondary_user()
        response = self.client.get(reverse(self.url_list), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertEqual(len(elements), 0)

    def test_other_user_see_detail_delivery(self):
        '''
        test with the main purpose that the user can see only own deliverys detail
        and not the others user's deliverys detail
        '''
        self.login_secondary_user()
        data = {
            "name": "other name"
        }
        response = self.client.get(
            reverse(self.url_detail, kwargs={'pk': self.delivery_id}),
            data
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_other_user_edit_delivery(self):
        '''
        test with the main purpose that the user can edit only own deliverys detail
        and not the others user's deliverys detail
        '''
        self.login_secondary_user()
        old_delivery = Delivery.objects.first()
        data = {
            "name": "other name"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.delivery_id}),
            data
        )
        after_delivery = Delivery.objects.first()
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(old_delivery.name, after_delivery.name)
        self.assertEqual(Delivery.objects.count(), 1)

    def test_other_user_delete_delivery(self):
        '''
        test with the main purpose that the user can delete only own deliverys
        and not the others user's deliverys
        '''
        self.login_secondary_user()
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.delivery_id})
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(Delivery.objects.count(), 1)

    def test_unauthorized_user_see_delivery_list(self):
        '''
        test with the main purpose that the anonymous user can't see deliverys
        '''
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_unauthorized_user_create_delivery(self):
        '''
        test with the main purpose that the anonymous user can't create
        deliverys
        '''
        data = {
            "name": "unauthorized user delivery"
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(Delivery.objects.count(), 1)

    def test_unauthorized_user_detail_delivery(self):
        '''
        test with the main purpose that the anonymous user can't see delivery's
        detail
        '''
        data = {
            "name": "other name"
        }
        response = self.client.get(
            reverse(self.url_detail, kwargs={'pk': self.delivery_id}),
            data
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_unauthorized_user_edit_delivery(self):
        '''
        test with the main purpose that the anonymous user can't edit delivery's
        detail
        '''
        old_delivery = Delivery.objects.first()
        data = {
            "name": "other name"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.delivery_id}),
            data
        )
        after_delivery = Delivery.objects.first()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(old_delivery.name, after_delivery.name)
        self.assertEqual(Delivery.objects.count(), 1)

    def test_unauthorized_user_delete_delivery(self):
        '''
        test with the main purpose that the anonymous user can't delete delivery's
        detail
        '''
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.delivery_id})
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.assertEqual(Delivery.objects.count(), 1)
