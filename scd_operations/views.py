
from rest_framework.decorators import api_view
import json
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from .data_definitions import PartialOperatorDataPayload
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
            o_d = PartialOperatorDataPayload(operator_data['uas_serial_number'],operation_mode = operator_data['operation_mode'], uas_class = operator_data['uav_class'], identification_technologies = operator_data['identification_technologies'],connectivity_methods = operator_data['connectivity_methods'],  endurance_minutes = operator_data['endurance_minutes'], emergency_procedure_url = operator_data['emergency_procedure_url'],operator_id = operator_data['operator_id'])

        except KeyError as ke:
            return Response({"message":"Could not parse payload, expected key %s not found " % ke }, status = status.HTTP_400_BAD_REQUEST)


        

        return Response({"message":"OK"}, status = status.HTTP_200_OK)