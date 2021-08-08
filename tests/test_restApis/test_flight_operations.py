from django.urls import reverse
from rest_framework import status

from .test_setup import TestApiEndpoints


class TestFlightOperations(TestApiEndpoints):
    fixtures = ['FlightOperation', 'Aircraft', 'FlightPlan', 'Activity', 'Operator', 'Manufacturer', 'TypeCertificate',
                'Engine', 'Address', 'Authorization', ]

    def setUp(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])

    def test_flight_operations_list_get_returns_200(self):
        url = reverse('flight-operation-list')

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()[0]['id'], self.get_pk_for_modal('FlightOperation'))

    def test_flight_operations_detail_get_returns_200(self):
        url = reverse('flight-operation-detail', kwargs={'pk': self.get_pk_for_modal('FlightOperation')})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['id'], self.get_pk_for_modal('FlightOperation'))

    def test_flight_operations_detail_get_returns_404(self):
        url = reverse('flight-operation-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})
