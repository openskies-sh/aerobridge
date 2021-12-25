from django.urls import reverse
from rest_framework import status

from .test_setup import TestApiEndpoints


class TestAircraft(TestApiEndpoints):
    fixtures = ['Aircraft', 'Operator', 'Manufacturer', 'TypeCertificate', 'Address', 'Authorization', 'Activity']

    def test_aircraft_list_returns_200(self):
        self.setUpClientCredentials([self.READ_SCOPE])
        url = reverse('aircraft-list')

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()[0]['id'], self.get_pk_for_model('Aircraft'))

    def test_aircraft_detail_returns_200(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('aircraft-detail', kwargs={'pk': self.get_pk_for_model('Aircraft')})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['id'], self.get_pk_for_model('Aircraft'))

    def test_aircraft_detail_returns_404(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('aircraft-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})

    def test_aircraft_rfm_detail_returns_200(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('aircraft-rfm-detail',
                      kwargs={'flight_controller_id': self.get_key_for_model('Aircraft', 'flight_controller_id')})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['id'], self.get_pk_for_model('Aircraft'))

    def test_aircraft_rfm_detail_returns_404(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('aircraft-rfm-detail', kwargs={'flight_controller_id': self.faker.word()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})
