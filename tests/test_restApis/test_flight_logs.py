from django.urls import reverse
from rest_framework import status

from .test_setup import TestApiEndpoints


class TestFlightLogs(TestApiEndpoints):
    fixtures = ['FlightLog', 'FlightOperation', 'Aircraft', 'FlightPlan', 'Activity', 'Operator', 'Manufacturer',
                'TypeCertificate', 'Engine', 'Address', 'Authorization']

    def setUp(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])

    def test_flight_log_list_get_returns_200(self):
        url = reverse('log-list')

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()[0]['id'], self.get_pk_for_modal('FlightLog'))

    def test_flight_log_list_post_returns_201(self):
        url = reverse('log-list')

        data = dict()
        data['operation'] = self.get_pk_for_modal('FlightOperation')
        data['signed_log'] = self.faker.uri()
        data['raw_log'] = self.faker.uri()

        required_keys = {'id', 'signed_log', 'raw_log', 'created_at', 'updated_at', 'operation', 'updated_at'}
        res = self.client.post(url, data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(res.json().keys()), required_keys)

    def test_flight_log_detail_get_returns_200(self):
        url = reverse('log-detail', kwargs={'pk': self.get_pk_for_modal('FlightLog')})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['id'], self.get_pk_for_modal('FlightLog'))

    def test_flight_log_detail_get_returns_404(self):
        url = reverse('log-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})

    def test_log_detail_put_returns_200(self):
        url = reverse('log-detail', kwargs={'pk': self.get_pk_for_modal('FlightLog')})

        data = dict()
        data['operation'] = self.get_pk_for_modal('FlightOperation')
        data['signed_log'] = self.faker.uri()
        data['raw_log'] = self.faker.uri()

        required_keys = {'id', 'signed_log', 'raw_log', 'created_at', 'updated_at', 'operation', 'updated_at'}
        res = self.client.put(url, data=data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(set(res.json().keys()), required_keys)

    def test_log_detail_delete_returns_200(self):
        url = reverse('log-detail', kwargs={'pk': self.get_pk_for_modal('FlightLog')})

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res.content, b'')

    def test_log_detail_delete_returns_404(self):
        url = reverse('log-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})
