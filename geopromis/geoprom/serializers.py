from rest_framework import serializers
from .models import Satellite,Session
from rest_framework.validators import ValidationError
from datetime import date
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import os
from django.contrib.auth.models import User
from rest_framework_gis.serializers import GeoFeatureModelSerializer




class UserSerializer(serializers.ModelSerializer):
    satellites = serializers.PrimaryKeyRelatedField(many=True, queryset=Satellite.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'satellites')

class SatelliteSerializer(serializers.ModelSerializer):
    """
    This class collects serialization methods for satellites and attributes from model Satellite
    """
    class Meta:
        model = Satellite
        fields = ('title', 'description','date_start','date_end')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Satellite.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance

class SessionSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Session
        geo_field = "geo_line"
        fields =('time_begin','time_end',)
    

    #owner = serializers.ReadOnlyField(source='owner.username')