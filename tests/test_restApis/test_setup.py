import json
import os

from cryptography.fernet import Fernet
from django.conf import settings

import requests
from faker import Faker
from rest_framework.test import APITransactionTestCase

from pki_framework.models import AerobridgeCredential
from gcs_operations.models import FlightLog


class TestApiEndpoints(APITransactionTestCase):
    data_path = os.getcwd() + '/tests/fixtures/'
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

    def fixAerobridgeCredentialData(self):
        """
        helper method to fix corrupted tokens during load data
        """
        fernet = Fernet(settings.CRYPTOGRAPHY_SALT.encode('utf-8'))
        test_rsa = b'-----BEGIN RSA PRIVATE KEY-----\n' \
                       b'MIICXAIBAAKBgQCUJiwW+B3j4V02jugKDsBkA0xhzFgajvJLzt97FGG/xuMGBV9O\n' \
                       b'Z+mRlpxw3kE4HnivDXASgyg5xdfiipgHBOSQqvXDLqp9s65tQXZsoFOrhS1cDeIk\n' \
                       b'AmAOh1IXLLGQO+oAxRUsqpu+j94VHP9peuiTtsyxfFAcj/psjP6bHlGDHwIDAQAB\n' \
                       b'AoGBAJE13S9iYYHUitYIOt5o2SDurraJYa4egNXXXuu37ZvZKPrk1yb16VV/h7WF\n' \
                       b'0+1ayLXkeP5cOlhuWI2/hQYUQKcal0nFQXCB/8+ynZJuFEwjkIwscKnGFt1MAteC\n' \
                       b'sBS1Ea3L0rDBiPtyqCz8PyCU9n5mt8K0waicf9he/41ykuvZAkEA7n/nFqpenYW9\n' \
                       b'9pXWz9aM1hvvj+JkfCDkL8fEhiTZW3R19OXau267nvH98BcmKjOkb/KgigytE6XQ\n' \
                       b'WUJv5kRF2wJBAJ8FFHZ8WbATX3RVre41MX6oFkBoYkE5SiQEwFuzUmJjch9lxq1U\n' \
                       b'Jo8DqSIbWLIbFTxAHFFzEM28OBDG3AUNFQ0CQC24AQF8SUTjBWZGlPYkh7zngAXR\n' \
                       b'/Tc6SuPJ5KdeWvhIG/CFO2fgs0Cl3OrwVRWT7rqzBQlRor/4cjcaID9A6S8CQH3U\n' \
                       b'1Dtp7MKCoe75eXdcSj0SHwF6V/2KqttTky8897z5Oi4UKCGxzA0w9V4Sy52sBqK1\n' \
                       b'jHL7HVnfTXIhGas5jeUCQGx2Y9ylz4wE6+QrumBC/GK2j6/PMrzCFKjPidw0bJ1G\n' \
                       b'OPMuWRXoeOj2kxnGSzXUUcsK2qLGqbHL8djYnaBK9HQ=\n' \
                       b'-----END RSA PRIVATE KEY-----'

        for i in range(AerobridgeCredential.objects.count()):
            # TODO: read token from AerobridgeCredential.json file
            token = fernet.encrypt(test_rsa)
            pk = self.get_pk_for_model('AerobridgeCredential', i)
            cred = AerobridgeCredential.objects.get(pk=pk)
            cred.token = token
            cred.save()

        # loaddata loading JSONField as string, converting data to json object
        for i in range(FlightLog.objects.count()):
            raw_log = self.get_key_for_model('FlightLog', 'raw_log', i)
            pk = self.get_pk_for_model('FlightLog', i)
            flight_log = FlightLog.objects.get(pk=pk)
            flight_log.raw_log = json.loads(raw_log)
            flight_log.save()


    def get_key_for_model(self, model_name, key_name, index=0):
        filepath = '%s%s.json' % (self.data_path, model_name)
        if os.path.exists(filepath):
            data = json.loads(open(filepath, 'r').read())
            if index < len(data):
                if key_name == 'pk':
                    return data[index]['pk']
                if key_name in data[index]['fields'].keys():
                    return data[index]['fields'][key_name]
                raise KeyError("Invalid key %s for index %d in model %s" % (key_name, index, model_name))
            else:
                raise IndexError("Invalid index %d for model %s" % (index, model_name))
        else:
            raise AssertionError("File %s.json does not exists in fixtures" % model_name)

    def get_pk_for_model(self, model_name, index=0):
        return self.get_key_for_model(model_name, 'pk', index)

    @classmethod
    def tearDownClass(cls):
        pass
