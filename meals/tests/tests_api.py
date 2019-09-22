import unittest
from django.urls import reverse
from rest_framework import status

from commons.tests import APITestBaseCase
from commons.constants import EMPTY_FIELD_ERROR_TEXT, TEXT_WITH_210_CHARACTERS,\
    get_maximum_error_text_in_field

from tags.models import Tag
from meals.models import Meal


@unittest.skip("skip for using views class")
class MealTest(APITestBaseCase):
    '''
    Tests belong to Meal functionality
    '''

    def setUp(self):
        '''
        urls and data initialization for testing
        '''
        self.url_list = 'meal-list'
        self.url_detail = 'meal-detail'
        self.meal_id = self.create_meal_for_principal_user(
            {"name": "first meal"})
        self.tag_id = self.create_tag_for_principal_user('first tag')
        self.second_tag_id = self.create_tag_for_principal_user('second tag')
        super(MealTest, self).setUp()

    def tearDown(self):
        """
        Remove and clean test data
        """
        Meal.objects.all().delete()
        super(MealTest, self).tearDown()

    def create_meal(self, name):
        '''
        create Meal for any user
        '''
        response = self.client.post(reverse(self.url_list), {"name": name})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        meal_id = response.json()['id']
        self.assertEqual(Meal.objects.filter(id=meal_id).count(), 1)
        return meal_id

    def test_same_user_see_meal_list(self):
        '''
        test with the main purpose that the user can see only own Meals
        '''
        self.login_principal_user()
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertEqual(len(elements), 1)

    def test_same_user_create_meal(self):
        '''
        test with the main purpose that the user can create a Meal
        '''
        self.login_principal_user()
        data = {
            "name": "other Meal"
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Meal.objects.count(), 2)

    def test_same_user_create_empty_meal(self):
        '''
        test with the main purpose to warn when Meal is created with an
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
        self.assertEqual(Meal.objects.count(), 1)

    def test_same_user_create_meal_maximum_characters(self):
        '''
        test with the main purpose to warn when Meal is created with an name
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
        self.assertEqual(Meal.objects.count(), 1)

    def test_create_meal_with_tag(self):
        '''
        test with the main purpose that the user can create a Meal with tag
        '''
        self.login_principal_user()
        data = {
            "name": "first meal",
            "tags": [self.tag_id]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        meal_id = response.json()['id']
        meal = Meal.objects.filter(id=meal_id)
        self.assertEqual(meal.count(), 1)
        self.assertEqual(meal.first().name, data['name'])
        self.assertEqual(meal.first().tags.count(), 1)
        self.assertIn('first tag', meal.first(
        ).tags.values_list('name', flat=True))

    def test_create_meal_with_empty_tag(self):
        '''
        test with the main purpose that the user can create a Meal with tag params but without tags
        '''
        self.login_principal_user()
        data = {
            "name": "first meal",
            "tags": []
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        meal_id = response.json()['id']
        meal = Meal.objects.filter(id=meal_id)
        self.assertEqual(meal.count(), 1)
        self.assertEqual(meal.first().name, data['name'])
        self.assertEqual(meal.first().tags.count(), 0)

    def test_create_meal_with_more_tags(self):
        '''
        test with the main purpose that the user can create a Meal with more tags
        '''
        self.login_principal_user()
        data = {
            "name": "first meal",
            "tags": [self.tag_id, self.second_tag_id]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        meal_id = response.json()['id']
        meal = Meal.objects.filter(id=meal_id)
        self.assertEqual(meal.count(), 1)
        self.assertEqual(meal.first().name, data['name'])
        self.assertEqual(meal.first().tags.count(), 2)
        self.assertIn('first tag', meal.first(
        ).tags.values_list('name', flat=True))
        self.assertIn('second tag', meal.first(
        ).tags.values_list('name', flat=True))

    def test_create_meal_with_non_exist_tag(self):
        '''
        test with the main purpose that the user can create a Meal with tag
        '''
        self.login_principal_user()
        data = {
            "name": "first meal withot tag",
            "tags": [4]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        meal_id = response.json()['id']
        meal = Meal.objects.filter(id=meal_id)
        self.assertEqual(meal.count(), 1)
        self.assertEqual(meal.first().name, data['name'])
        self.assertEqual(meal.first().tags.count(), 0)

    def test_same_user_edit_meal(self):
        '''
        test with the main purpose that the user can edit a Meal
        '''
        self.login_principal_user()
        old_meal = Meal.objects.first()
        data = {
            "name": "other Meal"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.meal_id}),
            data
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Meal.objects.count(), 1)
        new_meal = Meal.objects.first()
        self.assertEqual(new_meal.name, data['name'])
        self.assertNotEqual(old_meal.name, new_meal.name)

    def test_same_user_edit_empty_meal(self):
        '''
        test with the main purpose to warn when Meal is edit with an empty name
        '''
        self.login_principal_user()
        old_meal = Meal.objects.first()
        data = {
            "name": ""
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.meal_id}),
            data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Meal.objects.count(), 1)
        self.assertIn(
            EMPTY_FIELD_ERROR_TEXT,
            elements['name']
        )
        new_meal = Meal.objects.first()
        self.assertNotEqual(new_meal.name, data['name'])
        self.assertEqual(old_meal.name, new_meal.name)

    def test_same_user_edit_meal_maximum_characters(self):
        '''
        test with the main purpose to warn when Meal is edit with an name
        with more than the maximum characters
        '''
        self.login_principal_user()
        old_meal = Meal.objects.first()
        data = {
            "name": TEXT_WITH_210_CHARACTERS
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.meal_id}),
            data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Meal.objects.count(), 1)
        self.assertIn(
            get_maximum_error_text_in_field(200),
            elements['name']
        )
        new_meal = Meal.objects.first()
        self.assertNotEqual(new_meal.name, data['name'])
        self.assertEqual(old_meal.name, new_meal.name)

    def test_edit_meal_with_more_tags(self):
        '''
        test with the main purpose that the user can create a Meal with more tags
        '''
        self.login_principal_user()
        data = {
            "name": "first meal",
            "tags": []
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        meal_id = response.json()['id']
        meal = Meal.objects.filter(id=meal_id)
        self.assertEqual(meal.count(), 1)
        self.assertEqual(meal.first().name, data['name'])
        self.assertEqual(meal.first().tags.count(), 0)

        data = {
            "name": "first edit meal2",
            "tags": [self.tag_id, self.second_tag_id]
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': meal_id}),
            data
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        meal = Meal.objects.filter(id=meal_id)
        self.assertEqual(meal.first().tags.count(), 2)
        self.assertIn('first tag', meal.first(
        ).tags.values_list('name', flat=True))
        self.assertIn('second tag', meal.first(
        ).tags.values_list('name', flat=True))

    def test_edit_meal_with_more_tags_and_remove_one(self):
        '''
        test with the main purpose that the user can create a Meal with more tags
        '''
        self.login_principal_user()
        data = {
            "name": "first edit meal",
            "tags": [self.tag_id, self.second_tag_id]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        meal_id = response.json()['id']
        meal = Meal.objects.filter(id=meal_id)
        self.assertEqual(meal.count(), 1)
        self.assertEqual(meal.first().name, data['name'])
        self.assertEqual(meal.first().tags.count(), 2)
        self.assertIn('first tag', meal.first(
        ).tags.values_list('name', flat=True))
        self.assertIn('second tag', meal.first(
        ).tags.values_list('name', flat=True))

        data = {
            "name": "first edit meal2",
            "tags": [self.tag_id]
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': meal_id}),
            data
        )
        meal = Meal.objects.filter(id=meal.first().id)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(meal.count(), 1)
        self.assertEqual(meal.first().tags.count(), 1)
        self.assertIn('first tag', meal.first(
        ).tags.values_list('name', flat=True))

    def test_same_user_delete_meal(self):
        '''
        test with the main purpose that the user can delete a Meal
        '''
        self.login_principal_user()
        data = {
            "name": "other Meal"
        }
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.meal_id}),
            data
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Meal.objects.count(), 0)

    def test_remove_meal_with_more_tags(self):
        '''
        test with the main purpose that the user can delete a Meal with more tags
        '''
        self.login_principal_user()
        data = {
            "name": "first meal",
            "tags": [self.tag_id, self.second_tag_id]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        meal_id = response.json()['id']
        meal = Meal.objects.filter(id=meal_id)
        self.assertEqual(meal.count(), 1)
        self.assertEqual(meal.first().name, data['name'])
        self.assertEqual(meal.first().tags.count(), 2)
        self.assertIn('first tag', meal.first(
        ).tags.values_list('name', flat=True))
        self.assertIn('second tag', meal.first(
        ).tags.values_list('name', flat=True))

        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': meal_id})
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        meal = Meal.objects.filter(id=meal_id)
        self.assertEqual(meal.count(), 0)
        self.assertEqual(Tag.objects.count(), 2)

    def test_other_user_see_meal_list(self):
        '''
        test with the main purpose that the user can see only own Meals and no
        the other user's Meals
        '''
        self.login_secondary_user()
        response = self.client.get(reverse(self.url_list), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertEqual(len(elements), 0)

    def test_other_user_see_detail_meal(self):
        '''
        test with the main purpose that the user can see only own Meals detail
        and not the others user's Meals detail
        '''
        self.login_secondary_user()
        data = {
            "name": "other name"
        }
        response = self.client.get(
            reverse(self.url_detail, kwargs={'pk': self.meal_id}),
            data
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_other_user_edit_meal(self):
        '''
        test with the main purpose that the user can edit only own Meals detail
        and not the others user's Meals detail
        '''
        self.login_secondary_user()
        old_meal = Meal.objects.first()
        data = {
            "name": "other name"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.meal_id}),
            data
        )
        after_meal = Meal.objects.first()
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(old_meal.name, after_meal.name)
        self.assertEqual(Meal.objects.count(), 1)

    def test_other_user_delete_meal(self):
        '''
        test with the main purpose that the user can delete only own Meals
        and not the others user's Meals
        '''
        self.login_secondary_user()
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.meal_id})
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(Meal.objects.count(), 1)

    def test_unauthorized_user_see_meal_list(self):
        '''
        test with the main purpose that the anonymous user can't see Meals
        '''
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_unauthorized_user_create_meal(self):
        '''
        test with the main purpose that the anonymous user can't create
        Meals
        '''
        data = {
            "name": "unauthorized user Meal"
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(Meal.objects.count(), 1)

    def test_unauthorized_user_detail_meal(self):
        '''
        test with the main purpose that the anonymous user can't see Meal's
        detail
        '''
        data = {
            "name": "other name"
        }
        response = self.client.get(
            reverse(self.url_detail, kwargs={'pk': self.meal_id}),
            data
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_unauthorized_user_edit_meal(self):
        '''
        test with the main purpose that the anonymous user can't edit Meal's
        detail
        '''
        old_meal = Meal.objects.first()
        data = {
            "name": "other name"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.meal_id}),
            data
        )
        after_meal = Meal.objects.first()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(old_meal.name, after_meal.name)
        self.assertEqual(Meal.objects.count(), 1)

    def test_unauthorized_user_delete_meal(self):
        '''
        test with the main purpose that the anonymous user can't delete Meal's
        detail
        '''
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.meal_id})
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.assertEqual(Meal.objects.count(), 1)
