from django.urls import reverse
from rest_framework import status

from .test_setup import TestApiEndpoints


class TestManufacturer(TestApiEndpoints):
    fixtures = ['Manufacturer', 'Address']

    def test_manufacturer_list_returns_200(self):
        self.setUpClientCredentials([self.READ_SCOPE])
        url = reverse('manufacturer-list')

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()[0]['id'], self.get_pk_for_model('Manufacturer'))

    def test_manufacturer_detail_returns_200(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('manufacturer-detail', kwargs={'pk': self.get_pk_for_model('Manufacturer')})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['id'], self.get_pk_for_model('Manufacturer'))

    def test_manufacturer_detail_returns_404(self):
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])
        url = reverse('manufacturer-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})
