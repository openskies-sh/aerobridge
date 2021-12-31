from django.urls import reverse
from rest_framework import status

from .test_setup import TestApiEndpoints


class TestSignedFlightLogs(TestApiEndpoints):
    fixtures = ['SignedFlightLog', 'FlightLog', 'FlightOperation', 'FlightPlan', 'Activity', 'Authorization', 'Pilot',
                'Person', 'Operator', 'Address', 'Aircraft', 'Manufacturer']

    def setUp(self):
        self.setUpClientCredentials([self.READ_SCOPE])

    def test_signed_log_list_returns_200(self):
        url = reverse('signed-log-list')

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()[0]['id'], self.get_pk_for_model('SignedFlightLog'))

    def test_signed_log_detail_returns_200(self):
        url = reverse('signed-log-detail', kwargs={'pk': self.get_pk_for_model('SignedFlightLog')})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['id'], self.get_pk_for_model('SignedFlightLog'))

    def test_signed_log_detail_returns_404(self):
        url = reverse('signed-log-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})
