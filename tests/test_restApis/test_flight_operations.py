from datetime import datetime, timedelta

import pytz
from django.urls import reverse
from rest_framework import status

from gcs_operations.models import FlightOperation
from .test_setup import TestApiEndpoints


class TestFlightOperations(TestApiEndpoints):
    fixtures = ['FlightOperation', 'Aircraft', 'AircraftComponent', 'FlightPlan', 'Activity', 'Operator',
                'Manufacturer', 'Address', 'Authorization', 'Pilot', 'Person']

    @staticmethod
    def _patch_datetime(flight_operation):
        flight_operation.created_at = datetime.now(tz=pytz.UTC)
        flight_operation.start_datetime = datetime.now(tz=pytz.UTC) + timedelta(minutes=2)
        flight_operation.end_datetime = datetime.now(tz=pytz.UTC) + timedelta(minutes=40)
        flight_operation.save()

    def test_flight_operations_list_get_returns_200(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('flight-operation-list')

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()[0]['id'], self.get_pk_for_model('FlightOperation'))

    def test_flight_operations_list_post_returns_201(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('flight-operation-list')

        data = dict()
        data['name'] = self.faker.name()
        data['drone'] = self.get_pk_for_model('Aircraft')
        data['flight_plan'] = self.get_pk_for_model('FlightPlan')
        data['operator'] = self.get_pk_for_model('Operator')
        data['pilot'] = self.get_pk_for_model('Pilot')
        data['purpose'] = self.get_pk_for_model('Activity')

        required_keys = {'id', 'name', 'drone', 'flight_plan', 'operator', 'pilot', 'purpose', 'type_of_operation',
                         'created_at', 'start_datetime', 'end_datetime'}
        res = self.client.post(url, data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(res.json().keys()), required_keys)

    def test_flight_operations_detail_get_returns_200(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('flight-operation-detail', kwargs={'pk': self.get_pk_for_model('FlightOperation')})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['id'], self.get_pk_for_model('FlightOperation'))

    def test_flight_operations_detail_get_returns_404(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('flight-operation-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})

    def test_flight_operation_permission_unpatched_datetime_put_returns_400(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('flight-operation-permission', kwargs={'operation_id': self.get_pk_for_model('FlightOperation')})

        res = self.client.put(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json(), ['Cannot issue permissions for operations whose start time is in the past or '
                                      'more than a hour from now'])

    def test_flight_operation_permission_patched_datetime_put_returns_200(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('flight-operation-permission', kwargs={'operation_id': self.get_pk_for_model('FlightOperation')})
        self._patch_datetime(FlightOperation.objects.first())

        required_keys = {'id', 'operation', 'token', 'status_code', 'updated_at', 'created_at'}
        res = self.client.put(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(set(res.json().keys()), required_keys)

    def test_flight_operation_permission_put_returns_404(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('flight-operation-permission', kwargs={'operation_id': self.faker.uuid4()})

        res = self.client.put(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})
