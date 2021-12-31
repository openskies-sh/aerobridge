from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from .test_setup import TestApiEndpoints


class TestFlightPlans(TestApiEndpoints):
    fixtures = ['FlightPlan']

    def setUp(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])

    def test_flight_plan_list_get_returns_200(self):
        url = reverse('flight-plan-list')

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()[0]['id'], self.get_pk_for_model('FlightPlan'))

    def test_flight_plan_list_post_returns_201(self):
        url = reverse('flight-plan-list')

        data = dict()
        data['name'] = self.faker.word()
        data['plan_file_json'] = self.get_key_for_model('FlightPlan', 'plan_file_json')
        data['geo_json'] = self.get_key_for_model('FlightPlan', 'geo_json')

        required_keys = {'id', 'name', 'plan_file_json', 'created_at', 'updated_at'}
        res = self.client.post(url, data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(res.json().keys()), required_keys)

    def test_flight_plan_detail_get_returns_200(self):
        url = reverse('flight-plan-detail', kwargs={'pk': self.get_pk_for_model('FlightPlan')})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['id'], self.get_pk_for_model('FlightPlan'))

    def test_flight_plan_detail_get_returns_404(self):
        url = reverse('flight-plan-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})

    def test_flight_plan_detail_put_returns_200(self):
        url = reverse('flight-plan-detail', kwargs={'pk': self.get_pk_for_model('FlightPlan')})

        data = dict()
        data['name'] = self.faker.name()
        data['plan_file_json'] = self.get_key_for_model('FlightPlan', 'plan_file_json', 1)
        data['geo_json'] = self.get_key_for_model('FlightPlan', 'geo_json', 1)
        data['start_datetime'] = timezone.now()
        data['end_datetime'] = timezone.now() + timezone.timedelta(minutes=20)

        required_keys = {'id', 'name', 'plan_file_json', 'created_at', 'updated_at'}
        res = self.client.put(url, data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(set(res.json().keys()), required_keys)

    # TODO: Include this test
    def exclude_test_flight_plan_detail_delete_returns_204(self):
        url = reverse('flight-plan-detail', kwargs={'pk': self.get_pk_for_model('FlightPlan')})

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res.content, b'')

    # TODO: Include this test
    def exclude_test_flight_plan_detail_delete_returns_404(self):
        url = reverse('flight-plan-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})
