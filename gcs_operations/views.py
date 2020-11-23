from django.shortcuts import render
from rest_framework import mixins
from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from .serializers import DroneSerializer
from rest_framework import viewsets
from rest_framework import status
from .models import Drone

# Create your views here.


class DroneList(generics.ListAPIView):

    """
    List all drones, or create a new drone.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    

class DroneCreate(mixins.CreateModelMixin,
				  generics.GenericAPIView):
	
    

    queryset = Drone.objects.all()

    def create(self, request, *args, **kwargs):
        drone_id = self.kwargs['drone_id']		
        return Response({
        "drone_id": drone_id
        }, status=status.HTTP_201_CREATED) 

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a drone instance.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    
    