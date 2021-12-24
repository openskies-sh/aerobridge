import json

from django.urls import reverse
from rest_framework import status

from .test_setup import TestApiEndpoints


class TestHeartbeat(TestApiEndpoints):
    def setUp(self):
        self.url = reverse('ping')

    def test_ping_returns_200(self):
        res = self.client.get(self.url)
        content = json.loads(res.content)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get('message', None), 'pong')
