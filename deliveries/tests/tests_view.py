from datetime import date

from django.urls import reverse
from django.test import TestCase

from rest_framework import status

from freezegun import freeze_time

from commons.tests import UserLoginMixin
from commons.library import get_datetime
from commons.constants import EMPTY_FIELD_REQUIRED_TEXT_ES
from deliveries.models import Delivery, DeliverySelection
from menus.models import Menu
from distributions.models import Distribution
from plates.models import Plate
from meals.models import Meal
from deliveries.forms import DeliverySelectionForm


class TestDeliverySelection(TestCase, UserLoginMixin):
    '''
    Tests for verify behaviour for the commensals's answers
    '''
    def setUp(self):
        freezer = freeze_time('2012-01-14 03:21:34')
        freezer.start()
        self.nora = self.create_user(username='nora', is_staff=True)
        meal = Meal.objects.create(name="meal 1", owner=self.nora)
        self.plate_1 = Plate.objects.create(name="plate 1", owner=self.nora)
        self.plate_1.meals.add(meal)
        self.plate_2 = Plate.objects.create(name="plate 2", owner=self.nora)
        self.plate_2.meals.add(meal)
        self.distribution = Distribution.objects.create(
            name="test",
            link_id="link",
            is_active=True,
            distribution_hour_link=get_datetime(0),
            end_available_distribution_link=get_datetime(6),
            owner=self.nora,
        )
        self.menu = Menu.objects.create(
            owner=self.nora,
            name="test"
        )
        self.menu.plates.add(self.plate_1)
        self.menu.plates.add(self.plate_2)
        self.delivery = Delivery.objects.create(
            menu_delivery_id='02d9cf84-6ec9-4dca-bc2e-8eaee718927f',
            menu=self.menu,
            distribution=self.distribution,
            date=date.today(),
            owner=self.nora,
        )
        self.setup_logged_in_client()
        self.url = reverse(
            'delivery-selection',
            kwargs={
                'id': self.delivery.menu_delivery_id
            }
        )

    def tearDown(self):
        self.client.logout()
        Delivery.objects.all().delete()
        self.delete_all_user()

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertIsInstance(response.context_data['form'], DeliverySelectionForm)

    def test_form_errors(self):
        self.assertEqual(Delivery.objects.all().count(), 1)
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.context_data)
        self.assertEqual(len(response.context_data['form'].errors.keys()), 2)
        self.assertFormError(response, 'form', 'name', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertFormError(response, 'form', 'plates', EMPTY_FIELD_REQUIRED_TEXT_ES)
        self.assertEqual(DeliverySelection.objects.all().count(), 0)

    def test_create_successful(self):
        self.assertEqual(DeliverySelection.objects.all().count(), 0)
        data = {
            'name': 'Corchito',
            'description': 'no hay platos sin carne?? =(',
            'plates': [self.plate_1.id]
        }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'deliveries/thanks.html')
        self.assertEqual(DeliverySelection.objects.all().count(), 1)


class TestDeliveryAnonymous(TestCase, UserLoginMixin):

    def setUp(self):
        freezer = freeze_time('2012-01-14 03:21:34')
        freezer.start()
        self.nora = self.create_user(username='nora', is_staff=True)
        meal = Meal.objects.create(name="meal 1", owner=self.nora)
        plate_1 = Plate.objects.create(name="plate 1", owner=self.nora)
        plate_1.meals.add(meal)
        plate_2 = Plate.objects.create(name="plate 2", owner=self.nora)
        plate_2.meals.add(meal)
        self.distribution = Distribution.objects.create(
            name="test",
            link_id="link",
            is_active=True,
            distribution_hour_link=get_datetime(0),
            end_available_distribution_link=get_datetime(6),
            owner=self.nora,
        )
        self.menu = Menu.objects.create(
            owner=self.nora,
            name="test"
        )
        self.delivery = Delivery.objects.create(
            menu_delivery_id='02d9cf84-6ec9-4dca-bc2e-8eaee718927f',
            menu=self.menu,
            distribution=self.distribution,
            date=date.today(),
            owner=self.nora,
        )
        self.url = reverse(
            'delivery-selection',
            kwargs={
                'id': self.delivery.menu_delivery_id
            }
        )

    def test_get_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
