import os

import requests
from faker import Faker
from rest_framework.test import APITransactionTestCase

from ..aerobridge_tests_base import AerobridgeTestsBase


class TestApiEndpoints(APITransactionTestCase, AerobridgeTestsBase):
    READ_SCOPE = "aerobridge.read"
    WRITE_SCOPE = "aerobridge.write"

    @classmethod
    def setUpClass(cls):
        cls.faker = Faker()

    def setUpClientCredentials(self, scopes=None):
        if scopes.__class__ == list and self.READ_SCOPE not in scopes and self.WRITE_SCOPE not in scopes:
            return

        data = dict()
        data["client_id"] = os.getenv("PASSPORT_CLIENT_ID")
        data["client_secret"] = os.getenv("PASSPORT_CLIENT_SECRET")
        data["audience"] = os.getenv("PASSPORT_AUDIENCE")
        data["grant_type"] = "client_credentials"
        data["scope"] = " ".join(scopes)

        res = requests.post("https://id.openskies.sh/oauth/token/", data=data)
        type, token = res.json()['token_type'], res.json()['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='%s %s' % (type, token))

    @classmethod
    def tearDownClass(cls):
        pass
