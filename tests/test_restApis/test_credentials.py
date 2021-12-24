from django.urls import reverse
from rest_framework import status

from pki_framework.models import Operator
from .test_setup import TestApiEndpoints


class TestCredentials(TestApiEndpoints):
    fixtures = ['AerobridgeCredential', 'Aircraft', 'Manufacturer', 'Operator', 'Address', 'Authorization', 'Activity']

    def setUp(self):
        self.fixAerobridgeCredentialData()
        self.setUpClientCredentials([self.READ_SCOPE, self.WRITE_SCOPE])

    def test_credentials_list_get_returns_200(self):
        url = reverse('pki-credentials-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()[0]['id'], self.get_pk_for_model('AerobridgeCredential'))

    def test_credentials_list_post_returns_201(self):
        url = reverse('pki-credentials-list')

        data = dict()
        data['token'] = self.faker.text()
        data['name'] = self.faker.name()
        data['token_type'] = 1
        data['association'] = 0
        data['operator'] = Operator.objects.first().id

        required_keys = {'token', 'name', 'token_type', 'association', 'is_active', 'id', 'aircraft', 'manufacturer',
                         'operator'}
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(res.json().keys()), required_keys)

    def test_credentials_detail_get_returns_200(self):
        url = reverse('pki-credentials-detail', kwargs={'pk': self.get_pk_for_model('AerobridgeCredential')})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['id'], self.get_pk_for_model('AerobridgeCredential'))

    def test_credentials_detail_get_returns_404(self):
        url = reverse('pki-credentials-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})

    def test_credentials_detail_delete_returns_200(self):
        url = reverse('pki-credentials-detail', kwargs={'pk': self.get_pk_for_model('AerobridgeCredential')})

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res.content, b'')

    def test_credentials_detail_delete_returns_404(self):
        url = reverse('pki-credentials-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})
