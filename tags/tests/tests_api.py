import unittest
from django.urls import reverse
from rest_framework import status

from commons.tests import APITestBaseCase
from commons.constants import EMPTY_FIELD_ERROR_TEXT, TEXT_WITH_210_CHARACTERS,\
    get_maximum_error_text_in_field

from tags.models import Tag


@unittest.skip("skip for using views class")
class TagTest(APITestBaseCase):
    '''
    Tests belong to tag functionality
    '''

    def setUp(self):
        '''
        urls and data initialization for testing
        '''
        self.url_list = 'tag-list'
        self.url_detail = 'tag-detail'
        self.tag_id = self.create_tag_for_principal_user('first tag')
        super(TagTest, self).setUp()

    def tearDown(self):
        """
        Remove and clean test data
        """
        Tag.objects.all().delete()
        super(TagTest, self).tearDown()

    def test_same_user_see_tag_list(self):
        '''
        test with the main purpose that the user can see only own tags
        '''
        self.login_principal_user()
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertEqual(len(elements), 1)

    def test_same_user_create_tag(self):
        '''
        test with the main purpose that the user can create a tag
        '''
        self.login_principal_user()
        data = {
            "name": "other tag"
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Tag.objects.count(), 2)

    def test_same_user_create_empty_tag(self):
        '''
        test with the main purpose to warn when tag is created with an
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
        self.assertEqual(Tag.objects.count(), 1)

    def test_same_user_create_tag_maximum_characters(self):
        '''
        test with the main purpose to warn when tag is created with an name
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
        self.assertEqual(Tag.objects.count(), 1)

    def test_same_user_edit_tag(self):
        '''
        test with the main purpose that the user can edit a tag
        '''
        self.login_principal_user()
        old_tag = Tag.objects.first()
        data = {
            "name": "other tag"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.tag_id}),
            data
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Tag.objects.count(), 1)
        new_tag = Tag.objects.first()
        self.assertEqual(new_tag.name, data['name'])
        self.assertNotEqual(old_tag.name, new_tag.name)

    def test_same_user_edit_empty_tag(self):
        '''
        test with the main purpose to warn when tag is edit with an empty name
        '''
        self.login_principal_user()
        old_tag = Tag.objects.first()
        data = {
            "name": ""
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.tag_id}),
            data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertIn(
            EMPTY_FIELD_ERROR_TEXT,
            elements['name']
        )
        new_tag = Tag.objects.first()
        self.assertNotEqual(new_tag.name, data['name'])
        self.assertEqual(old_tag.name, new_tag.name)

    def test_same_user_edit_tag_maximum_characters(self):
        '''
        test with the main purpose to warn when tag is edit with an name
        with more than the maximum characters
        '''
        self.login_principal_user()
        old_tag = Tag.objects.first()
        data = {
            "name": TEXT_WITH_210_CHARACTERS
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.tag_id}),
            data
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        elements = response.json()
        self.assertTrue(elements)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertIn(
            get_maximum_error_text_in_field(200),
            elements['name']
        )
        new_tag = Tag.objects.first()
        self.assertNotEqual(new_tag.name, data['name'])
        self.assertEqual(old_tag.name, new_tag.name)

    def test_same_user_delete_tag(self):
        '''
        test with the main purpose that the user can delete a tag
        '''
        self.login_principal_user()
        data = {
            "name": "other tag"
        }
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.tag_id}),
            data
        )
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Tag.objects.count(), 0)

    def test_other_user_see_tag_list(self):
        '''
        test with the main purpose that the user can see only own tags and no
        the other user's tags
        '''
        self.login_secondary_user()
        response = self.client.get(reverse(self.url_list), format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        elements = response.json()
        self.assertEqual(len(elements), 0)

    def test_other_user_see_detail_tag(self):
        '''
        test with the main purpose that the user can see only own tags detail
        and not the others user's tags detail
        '''
        self.login_secondary_user()
        data = {
            "name": "other name"
        }
        response = self.client.get(
            reverse(self.url_detail, kwargs={'pk': self.tag_id}),
            data
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_other_user_edit_tag(self):
        '''
        test with the main purpose that the user can edit only own tags detail
        and not the others user's tags detail
        '''
        self.login_secondary_user()
        old_tag = Tag.objects.first()
        data = {
            "name": "other name"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.tag_id}),
            data
        )
        after_tag = Tag.objects.first()
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(old_tag.name, after_tag.name)
        self.assertEqual(Tag.objects.count(), 1)

    def test_other_user_delete_tag(self):
        '''
        test with the main purpose that the user can delete only own tags
        and not the others user's tags
        '''
        self.login_secondary_user()
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.tag_id})
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(Tag.objects.count(), 1)

    def test_unauthorized_user_see_tag_list(self):
        '''
        test with the main purpose that the anonymous user can't see tags
        '''
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_unauthorized_user_create_tag(self):
        '''
        test with the main purpose that the anonymous user can't create
        tags
        '''
        data = {
            "name": "unauthorized user tag"
        }
        response = self.client.post(reverse(self.url_list), data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(Tag.objects.count(), 1)

    def test_unauthorized_user_detail_tag(self):
        '''
        test with the main purpose that the anonymous user can't see tag's
        detail
        '''
        data = {
            "name": "other name"
        }
        response = self.client.get(
            reverse(self.url_detail, kwargs={'pk': self.tag_id}),
            data
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_unauthorized_user_edit_tag(self):
        '''
        test with the main purpose that the anonymous user can't edit tag's
        detail
        '''
        old_tag = Tag.objects.first()
        data = {
            "name": "other name"
        }
        response = self.client.put(
            reverse(self.url_detail, kwargs={'pk': self.tag_id}),
            data
        )
        after_tag = Tag.objects.first()
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(old_tag.name, after_tag.name)
        self.assertEqual(Tag.objects.count(), 1)

    def test_unauthorized_user_delete_tag(self):
        '''
        test with the main purpose that the anonymous user can't delete tag's
        detail
        '''
        response = self.client.delete(
            reverse(self.url_detail, kwargs={'pk': self.tag_id})
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        self.assertEqual(Tag.objects.count(), 1)
