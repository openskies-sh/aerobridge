
from rest_framework.decorators import api_view
import json
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from .data_definitions import FlightAuthorizationOperatorDataPayload, OperatorDataPayload
from .utils import UAVSerialNumberValidator, OperatorRegistrationNumberValidator
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

@api_view(['PUT'])
def operator_auth_test(request):
    return Response({"message":"OK"}, status = status.HTTP_200_OK)


class SCDAuthTest(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
    
    def put(self, request):
        
        operator_data = request.data
        
        try:
            operator_flight_authorization = operator_data['flight_authorisation']
            o_d = FlightAuthorizationOperatorDataPayload(uas_serial_number = operator_flight_authorization['uas_serial_number'],operation_category = operator_flight_authorization['operation_category'], operation_mode = operator_flight_authorization['operation_mode'], uas_class = operator_flight_authorization['uas_class'], identification_technologies = operator_flight_authorization['identification_technologies'],connectivity_methods = operator_flight_authorization['connectivity_methods'],  endurance_minutes = operator_flight_authorization['endurance_minutes'], emergency_procedure_url = operator_flight_authorization['emergency_procedure_url'],operator_id = operator_flight_authorization['operator_id'])
            
            operator_data_payload = OperatorDataPayload(priority=operator_data['priority'], flight_authorisation= o_d)

        except KeyError as ke:
            return Response({"result":"Could not parse payload, expected key %s not found " % ke }, status = status.HTTP_400_BAD_REQUEST)
        
        my_serial_number_validator = UAVSerialNumberValidator(serial_number = o_d.uas_serial_number)
        is_serial_number_valid = my_serial_number_validator.is_valid()
        if not is_serial_number_valid:
            return Response({"result":"Fail"}, status = status.HTTP_403_FORBIDDEN)


        my_reg_number_validator = OperatorRegistrationNumberValidator(operator_registration_number = o_d.operator_id)
        is_reg_number_valid = my_reg_number_validator.is_valid()
        if not is_reg_number_valid:
            return Response({"result":"Fail"}, status = status.HTTP_403_FORBIDDEN)

        

        return Response({"result":"Pass"}, status = status.HTTP_200_OK)