import json
import os

import requests
from faker import Faker
from rest_framework.test import APITransactionTestCase


class TestApiEndpoints(APITransactionTestCase):
    data_path = os.getcwd() + '/tests/fixtures/'
    READ_SCOPE = "aerobridge.read"
    WRITE_SCOPE = "aerobridge.write"

    @classmethod
    def setUpClass(cls):
        cls.faker = Faker()

    def setUpClientCredentials(self, scopes=[]):
        if self.READ_SCOPE not in scopes and self.WRITE_SCOPE not in scopes:
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

    def get_pk_for_modal(self, model_name, index=0):
        filepath = '%s%s.json' % (self.data_path, model_name)
        if os.path.exists(filepath):
            data = json.loads(open(filepath, 'r').read())
            return data[index]['pk']
        else:
            raise AssertionError("File %s.json does not exists in fixtures" % model_name)

    @classmethod
    def tearDownClass(cls):
        pass
