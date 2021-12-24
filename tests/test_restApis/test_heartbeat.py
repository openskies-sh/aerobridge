import json

from django.urls import reverse
from rest_framework import status

from .test_setup import TestApiEndpoints


class TestHeartbeat(TestApiEndpoints):
    def setUp(self):
        self.url = reverse('ping')

    def notest_ping_empty_scope_returns_401(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.json().get('detail', None), 'Authentication credentials were not provided')

    def notest_ping_write_scope_returns_403(self):
        self.setUpClientCredentials([self.WRITE_SCOPE])
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.json().get('message', None), 'You don\'t have access to this resource')

    def notest_ping_read_scope_returns_200(self):
        self.setUpClientCredentials([self.READ_SCOPE])
        res = self.client.get(self.url)
        content = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get('message', None), 'pong')

    def test_ping_returns_200(self):
        self.setUpClientCredentials([self.WRITE_SCOPE, self.READ_SCOPE])
        res = self.client.get(self.url)
        content = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get('message', None), 'pong')
