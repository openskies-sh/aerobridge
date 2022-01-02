from django.urls import reverse
from rest_framework import status

from .test_setup import TestApiEndpoints


class TestActivity(TestApiEndpoints):
    fixtures = ['Activity']

    def setUp(self):
        self.setUpClientCredentials([self.READ_SCOPE])

    def test_activity_list_returns_200(self):
        url = reverse('activity-list')

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()[0]['id'], self.get_pk_for_model('Activity'))

    def test_activity_detail_returns_200(self):
        url = reverse('activity-detail', kwargs={'pk': self.get_pk_for_model('Activity')})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['id'], self.get_pk_for_model('Activity'))

    def test_activity_detail_returns_404(self):
        url = reverse('activity-detail', kwargs={'pk': self.faker.uuid4()})

        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.json(), {'detail': 'Not found.'})
