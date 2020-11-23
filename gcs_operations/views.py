from django.shortcuts import render
from rest_framework import mixins
from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from .serializers import DroneSerializer
from rest_framework import status
from .models import Drone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import jwt
from functools import wraps
from django.http import JsonResponse

def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token

def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            print(token)
            decoded = jwt.decode(token, verify=False)
            print(decoded)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope

# Create your views here.

@api_view(['GET', 'POST'])
@requires_scope('aerobridge.write')
def drone_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        drones = Drone.objects.all()
        serializer = DroneSerializer(drones, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DroneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
@requires_scope('aerobridge.write')
def drone_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        drone = Drone.objects.get(pk=pk)
    except Drone.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DroneSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DroneSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)