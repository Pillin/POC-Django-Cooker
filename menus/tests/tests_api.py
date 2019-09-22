import unittest
from django.urls import reverse
from rest_framework import status

from commons.tests import APITestBaseCase
from commons.constants import EMPTY_FIELD_ERROR_TEXT, TEXT_WITH_210_CHARACTERS,\
    get_maximum_error_text_in_field

from plates.models import Plate
from menus.models import Menu


@unittest.skip("skip for using views class")
class MenuTest(APITestBaseCase):
    '''
    Tests belong to menu functionality
    '''

    def setUp(self):
        '''
        urls and data initialization for testing
        '''
        self.url_list = 'menu-list'
        self.url_detail = 'menu-detail'
        self.menu_id = self.create_menu_for_principal_user({"name": "firt menu"})
        self.unique_meal_id = self.create_meal_for_principal_user({"name": "first meal"})
        self.plate_id = self.create_plate_for_principal_user({
            "name": "first plate",
            "meals": [self.unique_meal_id]
        })
        self.second_meal_id = self.create_meal_for_principal_user({"name": "second meal"})
        self.second_plate_id = self.create_plate_for_principal_user({
            "name": "second plate",
            "meals": [self.second_meal_id]
        })
        super(MenuTest, self).setUp()

    def tearDown(self):
        """
        Remove and clean test data
        """
        Menu.objects.all().delete()
        super(MenuTest, self).tearDown()

    def create_menu(self, name):
        '''
        create menu for any user
        '''
        response = self.client.post(reverse(self.url_list), {"name": name})
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        menu_id = response.json()['id']
        self.assertEqual(Menu.objects.filter(id=menu_id).count(), 1)
        return menu_id

    def test_same_user_see_menu_list(self):
        '''
        test with the main purpose that the user can see only own menus
        '''
        self.login_principal_user()
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertEqual(len(elements), 1)

    def test_same_user_create_menu(self):
        '''
        test with the main purpose that the user can create a menu
        '''
        self.login_principal_user()
        data = {
            "name": "other menu"
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Menu.objects.count(), 2)

    def test_same_user_create_empty_menu(self):
        '''
        test with the main purpose to warn when menu is created with an
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
        self.assertEqual(Menu.objects.count(), 1)

    def test_same_user_create_menu_maximum_characters(self):
        '''
        test with the main purpose to warn when menu is created with an name
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
        self.assertEqual(Menu.objects.count(), 1)

    def test_create_menu_with_plate(self):
        '''
        test with the main purpose that the user can create a menu with plate
        '''
        self.login_principal_user()
        data = {
            "name": "first menu",
            "plates": [self.plate_id]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        menu_id = response.json()['id']
        menu = Menu.objects.filter(id=menu_id)
        self.assertEqual(menu.count(), 1)
        self.assertEqual(menu.first().name, data['name'])
        self.assertEqual(menu.first().plates.count(), 1)
        self.assertIn('first plate', menu.first(
        ).plates.values_list('name', flat=True))

    def test_create_menu_with_empty_plate(self):
        '''
        test with the main purpose that the user can create a menu with plate params but without plates
        '''
        self.login_principal_user()
        data = {
            "name": "first menu",
            "plates": []
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        menu_id = response.json()['id']
        menu = Menu.objects.filter(id=menu_id)
        self.assertEqual(menu.count(), 1)
        self.assertEqual(menu.first().name, data['name'])
        self.assertEqual(menu.first().plates.count(), 0)

    def test_create_menu_with_more_plates(self):
        '''
        test with the main purpose that the user can create a menu with more plates
        '''
        self.login_principal_user()
        data = {
            "name": "first menu",
            "plates": [self.plate_id, self.second_plate_id]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        menu_id = response.json()['id']
        menu = Menu.objects.filter(id=menu_id)
        self.assertEqual(menu.count(), 1)
        self.assertEqual(menu.first().name, data['name'])
        self.assertEqual(menu.first().plates.count(), 2)
        self.assertIn('first plate', menu.first(
        ).plates.values_list('name', flat=True))
        self.assertIn('second plate', menu.first(
        ).plates.values_list('name', flat=True))

    def test_create_menu_with_non_exist_plate(self):
        '''
        test with the main purpose that the user can create a menu with plate
        '''
        self.login_principal_user()
        data = {
            "name": "first menu withot plate",
            "plates": [4]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        menu_id = response.json()['id']
        menu = Menu.objects.filter(id=menu_id)
        self.assertEqual(menu.count(), 1)
        self.assertEqual(menu.first().name, data['name'])
        self.assertEqual(menu.first().plates.count(), 0)

    def test_same_user_edit_menu(self):
        '''
        test with the main purpose that the user can edit a menu
        '''
        self.login_principal_user()
        old_menu = Menu.objects.first()
        data = {
            "name": "other menu"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.menu_id}),
            data
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Menu.objects.count(), 1)
        new_menu = Menu.objects.first()
        self.assertEqual(new_menu.name, data['name'])
        self.assertNotEqual(old_menu.name, new_menu.name)

    def test_same_user_edit_empty_menu(self):
        '''
        test with the main purpose to warn when menu is edit with an empty name
        '''
        self.login_principal_user()
        old_menu = Menu.objects.first()
        data = {
            "name": ""
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.menu_id}),
            data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertIn(
            EMPTY_FIELD_ERROR_TEXT,
            elements['name']
        )
        new_menu = Menu.objects.first()
        self.assertNotEqual(new_menu.name, data['name'])
        self.assertEqual(old_menu.name, new_menu.name)

    def test_same_user_edit_menu_maximum_characters(self):
        '''
        test with the main purpose to warn when menu is edit with an name
        with more than the maximum characters
        '''
        self.login_principal_user()
        old_menu = Menu.objects.first()
        data = {
            "name": TEXT_WITH_210_CHARACTERS
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.menu_id}),
            data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertIn(
            get_maximum_error_text_in_field(200),
            elements['name']
        )
        new_menu = Menu.objects.first()
        self.assertNotEqual(new_menu.name, data['name'])
        self.assertEqual(old_menu.name, new_menu.name)

    def test_edit_menu_with_more_plates(self):
        '''
        test with the main purpose that the user can create a menu with more plates
        '''
        self.login_principal_user()
        data = {
            "name": "first menu",
            "plates": []
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        menu_id = response.json()['id']
        menu = Menu.objects.filter(id=menu_id)
        self.assertEqual(menu.count(), 1)
        self.assertEqual(menu.first().name, data['name'])
        self.assertEqual(menu.first().plates.count(), 0)

        data = {
            "name": "first edit menu2",
            "plates": [self.plate_id, self.second_plate_id]
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': menu_id}),
            data
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        menu = Menu.objects.filter(id=menu_id)
        self.assertEqual(menu.first().plates.count(), 2)
        self.assertIn('first plate', menu.first(
        ).plates.values_list('name', flat=True))
        self.assertIn('second plate', menu.first(
        ).plates.values_list('name', flat=True))

    def test_edit_menu_with_more_plates_and_remove_one(self):
        '''
        test with the main purpose that the user can create a menu with more plates
        '''
        self.login_principal_user()
        data = {
            "name": "first edit menu",
            "plates": [self.plate_id, self.second_plate_id]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        menu_id = response.json()['id']
        menu = Menu.objects.filter(id=menu_id)
        self.assertEqual(menu.count(), 1)
        self.assertEqual(menu.first().name, data['name'])
        self.assertEqual(menu.first().plates.count(), 2)
        self.assertIn('first plate', menu.first(
        ).plates.values_list('name', flat=True))
        self.assertIn('second plate', menu.first(
        ).plates.values_list('name', flat=True))

        data = {
            "name": "first edit menu2",
            "plates": [self.plate_id]
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': menu_id}),
            data
        )
        menu = Menu.objects.filter(id=menu.first().id)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(menu.count(), 1)
        self.assertEqual(menu.first().plates.count(), 1)
        self.assertIn('first plate', menu.first(
        ).plates.values_list('name', flat=True))

    def test_same_user_delete_menu(self):
        '''
        test with the main purpose that the user can delete a menu
        '''
        self.login_principal_user()
        data = {
            "name": "other menu"
        }
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.menu_id}),
            data
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Menu.objects.count(), 0)

    def test_remove_menu_with_more_plates(self):
        '''
        test with the main purpose that the user can delete a menu with more plates
        '''
        self.login_principal_user()
        data = {
            "name": "first menu",
            "plates": [self.plate_id, self.second_plate_id]
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        menu_id = response.json()['id']
        menu = Menu.objects.filter(id=menu_id)
        self.assertEqual(menu.count(), 1)
        self.assertEqual(menu.first().name, data['name'])
        self.assertEqual(menu.first().plates.count(), 2)
        self.assertIn('first plate', menu.first(
        ).plates.values_list('name', flat=True))
        self.assertIn('second plate', menu.first(
        ).plates.values_list('name', flat=True))

        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': menu_id})
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        menu = Menu.objects.filter(id=menu_id)
        self.assertEqual(menu.count(), 0)
        self.assertEqual(Plate.objects.count(), 2)

    def test_other_user_see_menu_list(self):
        '''
        test with the main purpose that the user can see only own menus and no
        the other user's menus
        '''
        self.login_secondary_user()
        response = self.client.get(reverse(self.url_list), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertEqual(len(elements), 0)

    def test_other_user_see_detail_menu(self):
        '''
        test with the main purpose that the user can see only own menus detail
        and not the others user's menus detail
        '''
        self.login_secondary_user()
        data = {
            "name": "other name"
        }
        response = self.client.get(
            reverse(self.url_detail, kwargs={'pk': self.menu_id}),
            data
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_other_user_edit_menu(self):
        '''
        test with the main purpose that the user can edit only own menus detail
        and not the others user's menus detail
        '''
        self.login_secondary_user()
        old_menu = Menu.objects.first()
        data = {
            "name": "other name"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.menu_id}),
            data
        )
        after_menu = Menu.objects.first()
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(old_menu.name, after_menu.name)
        self.assertEqual(Menu.objects.count(), 1)

    def test_other_user_delete_menu(self):
        '''
        test with the main purpose that the user can delete only own menus
        and not the others user's menus
        '''
        self.login_secondary_user()
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.menu_id})
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(Menu.objects.count(), 1)

    def test_unauthorized_user_see_menu_list(self):
        '''
        test with the main purpose that the anonymous user can't see menus
        '''
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_unauthorized_user_create_menu(self):
        '''
        test with the main purpose that the anonymous user can't create
        menus
        '''
        data = {
            "name": "unauthorized user menu"
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(Menu.objects.count(), 1)

    def test_unauthorized_user_detail_menu(self):
        '''
        test with the main purpose that the anonymous user can't see menu's
        detail
        '''
        data = {
            "name": "other name"
        }
        response = self.client.get(
            reverse(self.url_detail, kwargs={'pk': self.menu_id}),
            data
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_unauthorized_user_edit_menu(self):
        '''
        test with the main purpose that the anonymous user can't edit menu's
        detail
        '''
        old_menu = Menu.objects.first()
        data = {
            "name": "other name"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.menu_id}),
            data
        )
        after_menu = Menu.objects.first()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(old_menu.name, after_menu.name)
        self.assertEqual(Menu.objects.count(), 1)

    def test_unauthorized_user_delete_menu(self):
        '''
        test with the main purpose that the anonymous user can't delete menu's
        detail
        '''
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.menu_id})
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.assertEqual(Menu.objects.count(), 1)
