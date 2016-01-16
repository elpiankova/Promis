from geoprom.models import Satellite,Session
from geoprom.serializers import SatelliteSerializer,SessionSerializer
from django.http import Http404
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import generics
from geoprom.serializers import UserSerializer
from rest_framework import permissions

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SatelliteList(APIView):
    """
    List all satellites, or create a new satellite.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def get(self, request, format=None):
        satellites = Satellite.objects.all()
        serializer = SatelliteSerializer(satellites, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SatelliteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SatelliteDetail(APIView):
    """
    Retrieve, update or delete a satellite instance.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def get_object(self, pk):
        try:
            return Satellite.objects.get(pk=pk)
        except Satellite.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        satellite = self.get_object(pk)
        serializer = SatelliteSerializer(satellite)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        satellite = self.get_object(pk)
        serializer = SatelliteSerializer(satellite, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        satellite = self.get_object(pk)
        satellite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SatelliteSession(APIView):
    """
    Retrieve, session instance.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def get_object(self, pk):
        try:
            return Session.objects.get(pk=pk)
        except Satellite.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        session = self.get_object(pk)
        serializer = SessionSerializer(session)
        return Response(serializer.data)
