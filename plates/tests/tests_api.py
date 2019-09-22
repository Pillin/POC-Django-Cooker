import unittest
from django.urls import reverse
from rest_framework import status

from commons.tests import APITestBaseCase
from commons.constants import EMPTY_FIELD_ERROR_TEXT, TEXT_WITH_210_CHARACTERS,\
    get_maximum_error_text_in_field

from meals.models import Meal
from plates.models import Plate


@unittest.skip("skip for using views class")
class PlateTest(APITestBaseCase):
    '''
    Tests belong to plate functionality
    '''

    def setUp(self):
        '''
        urls and data initialization for testing
        '''
        self.url_list = 'plate-list'
        self.url_detail = 'plate-detail'
        self.unique_meal_id = self.create_meal_for_principal_user(
            {"name": "second meal"})
        self.plate_id = self.create_plate_for_principal_user({
            "name": "first plate",
            "meals": [self.unique_meal_id]
        })
        self.meal_id = self.create_meal_for_principal_user(
            {"name": "first meal"})
        self.second_meal_id = self.create_meal_for_principal_user(
            {"name": "second meal"})
        super(PlateTest, self).setUp()

    def tearDown(self):
        """
        Remove and clean test data
        """
        Meal.objects.all().delete()
        Plate.objects.all().delete()
        super(PlateTest, self).tearDown()

    def test_same_user_see_plate_list(self):
        '''
        test with the main purpose that the user can see only own plates
        '''
        self.login_principal_user()
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertEqual(len(elements), 1)

    def test_same_user_create_plate(self):
        '''
        test with the main purpose that the user can create a plate
        '''
        self.login_principal_user()
        data = {
            "name": "other plate"
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        elements = response.json()
        self.assertTrue(elements)

        self.assertEqual(Plate.objects.count(), 2)

    def test_same_user_create_empty_plate(self):
        '''
        test with the main purpose to warn when plate is created with an
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
        self.assertEqual(Plate.objects.count(), 1)

    def test_same_user_create_plate_maximum_characters(self):
        '''
        test with the main purpose to warn when plate is created with an name
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
        self.assertEqual(Plate.objects.count(), 1)

    def test_create_plate_with_meal(self):
        '''
        test with the main purpose that the user can create a plate with meal
        '''
        self.login_principal_user()
        data = {
            "name": "first plate",
            "meals": [self.meal_id]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        plate_id = response.json()['id']
        plate = Plate.objects.filter(id=plate_id)
        self.assertEqual(plate.count(), 1)
        self.assertEqual(plate.first().name, data['name'])
        self.assertEqual(plate.first().meals.count(), 1)
        self.assertIn('first meal', plate.first(
        ).meals.values_list('name', flat=True))

    def test_create_plate_with_empty_meal(self):
        '''
        test with the main purpose that the user can create a plate with meal params but without meals
        '''
        self.login_principal_user()
        data = {
            "name": "first plate",
            "meals": []
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Plate.objects.count(), 2)

    def test_create_plate_with_more_meals(self):
        '''
        test with the main purpose that the user can create a plate with more meals
        '''
        self.login_principal_user()
        data = {
            "name": "first plate",
            "meals": [self.meal_id, self.second_meal_id]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        plate_id = response.json()['id']
        plate = Plate.objects.filter(id=plate_id)
        self.assertEqual(plate.count(), 1)
        self.assertEqual(plate.first().name, data['name'])
        self.assertEqual(plate.first().meals.count(), 2)
        self.assertIn('first meal', plate.first(
        ).meals.values_list('name', flat=True))
        self.assertIn('second meal', plate.first(
        ).meals.values_list('name', flat=True))

    def test_create_plate_with_non_exist_meal(self):
        '''
        test with the main purpose that the user can create a plate with meal
        '''
        self.login_principal_user()
        data = {
            "name": "first plate withot meal",
            "meals": [4]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        plate_id = response.json()['id']
        plate = Plate.objects.filter(id=plate_id)
        self.assertEqual(plate.count(), 1)
        self.assertEqual(plate.first().name, data['name'])
        self.assertEqual(plate.first().meals.count(), 0)

    def test_same_user_edit_plate(self):
        '''
        test with the main purpose that the user can edit a plate
        '''
        self.login_principal_user()
        old_plate = Plate.objects.first()
        data = {
            "name": "other plate"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.plate_id}),
            data
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Plate.objects.count(), 1)
        new_plate = Plate.objects.first()
        self.assertEqual(new_plate.name, data['name'])
        self.assertNotEqual(old_plate.name, new_plate.name)

    def test_same_user_edit_empty_plate(self):
        '''
        test with the main purpose to warn when plate is edit with an empty name
        '''
        self.login_principal_user()
        old_plate = Plate.objects.first()
        data = {
            "name": ""
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.plate_id}),
            data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Plate.objects.count(), 1)
        self.assertIn(
            EMPTY_FIELD_ERROR_TEXT,
            elements['name']
        )
        new_plate = Plate.objects.first()
        self.assertNotEqual(new_plate.name, data['name'])
        self.assertEqual(old_plate.name, new_plate.name)

    def test_same_user_edit_plate_maximum_characters(self):
        '''
        test with the main purpose to warn when plate is edit with an name
        with more than the maximum characters
        '''
        self.login_principal_user()
        old_plate = Plate.objects.first()
        data = {
            "name": TEXT_WITH_210_CHARACTERS
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.plate_id}),
            data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Plate.objects.count(), 1)
        self.assertIn(
            get_maximum_error_text_in_field(200),
            elements['name']
        )
        new_plate = Plate.objects.first()
        self.assertNotEqual(new_plate.name, data['name'])
        self.assertEqual(old_plate.name, new_plate.name)

    def test_edit_plate_with_more_meals(self):
        '''
        test with the main purpose that the user can create a plate with more meals
        '''
        self.login_principal_user()
        data = {
            "name": "first plate",
            "meals": []
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        plate_id = response.json()['id']
        plate = Plate.objects.filter(id=plate_id)
        self.assertEqual(plate.count(), 1)
        self.assertEqual(plate.first().name, data['name'])
        self.assertEqual(plate.first().meals.count(), 0)

        data = {
            "name": "first edit plate2",
            "meals": [self.meal_id, self.second_meal_id]
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': plate_id}),
            data
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        plate = Plate.objects.filter(id=plate_id)
        self.assertEqual(plate.first().meals.count(), 2)
        self.assertIn('first meal', plate.first(
        ).meals.values_list('name', flat=True))
        self.assertIn('second meal', plate.first(
        ).meals.values_list('name', flat=True))

    def test_edit_plate_with_more_meals_and_remove_one(self):
        '''
        test with the main purpose that the user can create a plate with more meals
        '''
        self.login_principal_user()
        data = {
            "name": "first edit plate",
            "meals": [self.meal_id, self.second_meal_id]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        plate_id = response.json()['id']
        plate = Plate.objects.filter(id=plate_id)
        self.assertEqual(plate.count(), 1)
        self.assertEqual(plate.first().name, data['name'])
        self.assertEqual(plate.first().meals.count(), 2)
        self.assertIn('first meal', plate.first(
        ).meals.values_list('name', flat=True))
        self.assertIn('second meal', plate.first(
        ).meals.values_list('name', flat=True))

        data = {
            "name": "first edit plate2",
            "meals": [self.meal_id]
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': plate_id}),
            data
        )
        plate = Plate.objects.filter(id=plate.first().id)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(plate.count(), 1)
        self.assertEqual(plate.first().meals.count(), 1)
        self.assertIn('first meal', plate.first(
        ).meals.values_list('name', flat=True))

    def test_same_user_delete_plate(self):
        '''
        test with the main purpose that the user can delete a plate
        '''
        self.login_principal_user()
        data = {
            "name": "other plate"
        }
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.plate_id}),
            data
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Plate.objects.count(), 0)

    def test_remove_plate_with_more_meals(self):
        '''
        test with the main purpose that the user can delete a plate with more meals
        '''
        self.login_principal_user()
        data = {
            "name": "first plate",
            "meals": [self.meal_id, self.second_meal_id]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        plate_id = response.json()['id']
        plate = Plate.objects.filter(id=plate_id)
        self.assertEqual(plate.count(), 1)
        self.assertEqual(plate.first().name, data['name'])
        self.assertEqual(plate.first().meals.count(), 2)
        self.assertIn('first meal', plate.first(
        ).meals.values_list('name', flat=True))
        self.assertIn('second meal', plate.first(
        ).meals.values_list('name', flat=True))

        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': plate_id})
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        plate = Plate.objects.filter(id=plate_id)
        self.assertEqual(plate.count(), 0)
        self.assertEqual(Meal.objects.count(), 3)

    def test_other_user_see_plate_list(self):
        '''
        test with the main purpose that the user can see only own plates and no
        the other user's plates
        '''
        self.login_secondary_user()
        response = self.client.get(reverse(self.url_list), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertEqual(len(elements), 0)

    def test_other_user_see_detail_plate(self):
        '''
        test with the main purpose that the user can see only own plates detail
        and not the others user's plates detail
        '''
        self.login_secondary_user()
        data = {
            "name": "other name"
        }
        response = self.client.get(
            reverse(self.url_detail, kwargs={'pk': self.plate_id}),
            data
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_other_user_edit_plate(self):
        '''
        test with the main purpose that the user can edit only own plates detail
        and not the others user's plates detail
        '''
        self.login_secondary_user()
        old_plate = Plate.objects.first()
        data = {
            "name": "other name"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.plate_id}),
            data
        )
        after_plate = Plate.objects.first()
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(old_plate.name, after_plate.name)
        self.assertEqual(Plate.objects.count(), 1)

    def test_other_user_delete_plate(self):
        '''
        test with the main purpose that the user can delete only own plates
        and not the others user's plates
        '''
        self.login_secondary_user()
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.plate_id})
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(Plate.objects.count(), 1)

    def test_unauthorized_user_see_plate_list(self):
        '''
        test with the main purpose that the anonymous user can't see plates
        '''
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_unauthorized_user_create_plate(self):
        '''
        test with the main purpose that the anonymous user can't create
        plates
        '''
        data = {
            "name": "unauthorized user plate"
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(Plate.objects.count(), 1)

    def test_unauthorized_user_detail_plate(self):
        '''
        test with the main purpose that the anonymous user can't see plate's
        detail
        '''
        data = {
            "name": "other name"
        }
        response = self.client.get(
            reverse(self.url_detail, kwargs={'pk': self.plate_id}),
            data
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_unauthorized_user_edit_plate(self):
        '''
        test with the main purpose that the anonymous user can't edit plate's
        detail
        '''
        old_plate = Plate.objects.first()
        data = {
            "name": "other name"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.plate_id}),
            data
        )
        after_plate = Plate.objects.first()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(old_plate.name, after_plate.name)
        self.assertEqual(Plate.objects.count(), 1)

    def test_unauthorized_user_delete_plate(self):
        '''
        test with the main purpose that the anonymous user can't delete plate's
        detail
        '''
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.plate_id})
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.assertEqual(Plate.objects.count(), 1)
