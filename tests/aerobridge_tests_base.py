import json
import os

from gcs_operations.models import FlightLog
from pki_framework.models import AerobridgeCredential


class AerobridgeTestsBase(object):
    """
    Helper class for Aerobridge tests
    """
    data_path = os.getcwd() + '/tests/fixtures/'

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

    def _fix_aerobridge_credentials_token(self):
        """
        helper method to fix corrupted tokens during load data
        """
        for i in range(AerobridgeCredential.objects.count()):
            # TODO: read token from AerobridgeCredential.json file
            token = self.get_key_for_model('AerobridgeCredential', 'token', i)
            pk = self.get_pk_for_model('AerobridgeCredential', i)
            cred = AerobridgeCredential.objects.get(pk=pk)
            cred.token = token.encode()
            cred.save()

    def _fix_flight_log_raw_log(self):
        # loaddata loading JSONField as string, converting data to json object
        for i in range(FlightLog.objects.count()):
            raw_log = self.get_key_for_model('FlightLog', 'raw_log', i)
            pk = self.get_pk_for_model('FlightLog', i)
            flight_log = FlightLog.objects.get(pk=pk)
            flight_log.raw_log = json.loads(raw_log)
            flight_log.save()

    def fix_fixtures_data(self):
        self._fix_aerobridge_credentials_token()
        self._fix_flight_log_raw_log()
