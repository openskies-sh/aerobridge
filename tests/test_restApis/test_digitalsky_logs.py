from django.urls import reverse
from rest_framework import status

from .test_setup import TestApiEndpoints


class TestDigitalSkyLog(TestApiEndpoints):
    fixtures = ['DigitalSkyLog', 'Transaction', 'Aircraft', 'Engine', 'Operator', 'Manufacturer', 'TypeCertificate',
                'Address', 'Authorization', 'Activity']

    def setUp(self):
        self.setUpClientCredentials([self.READ_SCOPE])

    def test_digitalsky_log_list_returns_200(self):
        url = reverse('digitalsky-log-list')

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()[0]['id'], self.get_pk_for_model('DigitalSkyLog'))

    def test_digitalsky_log_detail_returns_200(self):
        url = reverse('digitalsky-log-detail', kwargs={'pk': self.get_pk_for_model('DigitalSkyLog')})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['id'], self.get_pk_for_model('DigitalSkyLog'))

    def test_digitalsky_log_detail_returns_404(self):
        url = reverse('digitalsky-log-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})
