from django.urls import reverse
from rest_framework import status

from .test_setup import TestApiEndpoints


class TestFirmware(TestApiEndpoints):
    fixtures = ['Firmware', 'Manufacturer', 'Address']

    def setUp(self):
        self.setUpClientCredentials([self.READ_SCOPE])

    def test_firmware_list_get_returns_200(self):
        url = reverse('firmware-list')

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()[0]['id'], self._get_pk_for_modal('Firmware'))

    def test_firmware_list_post_returns_201(self):
        url = reverse('firmware-list')

        data = dict()
        data['binary_file_url'] = self.faker.uri()
        data['public_key'] = self.faker.text()
        data['version'] = self.faker.pyfloat(min_value=0, max_value=10.00, right_digits=2)
        data['manufacturer'] = self._get_pk_for_modal('Manufacturer')
        data['friendly_name'] = self.faker.sentence(nb_words=4)
        data['is_active'] = True

        required_keys = {'id', 'binary_file_url', 'public_key', 'version', 'friendly_name', 'is_active', 'manufacturer',
                         'created_at', 'updated_at'}
        res = self.client.post(url, data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(res.json().keys()), required_keys)

    def test_firmware_detial_get_returns_200(self):
        url = reverse('firmware-detail', kwargs={'pk': self._get_pk_for_modal('Firmware')})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['id'], self._get_pk_for_modal('Firmware'))

    def test_firmware_detial_get_returns_404(self):
        url = reverse('firmware-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})
