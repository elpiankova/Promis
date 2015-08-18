from rest_framework import serializers
from .models import Device, DeviceMode, Request, DeviceSwitch
from rest_framework.validators import ValidationError
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
import os

class DeviceModeSerializer(serializers.ModelSerializer):
    """
    This class collects serialization methods for device modes and attributes from model DeviceMode
    """
    class Meta:
        model = DeviceMode
        fields = ('name', 'code', 'data_speed', 'power')


class DeviceSerializer(serializers.ModelSerializer):
    """
    This class collects serialization methods for devices and attributes from model Device
    """
    modes = DeviceModeSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ('name', 'code', 'modes')


class DeviceSwitchSerializer(serializers.ModelSerializer):
    """
    This class collects serialization methods for device switches and attributes from model DeviceSwitch
    """
    device = serializers.SlugRelatedField(slug_field='name', queryset=Device.objects.all())
    mode = serializers.SlugRelatedField(slug_field='name', queryset=DeviceMode.objects.all())
    request_number = serializers.IntegerField(source='request.number')

    class Meta:
        model = DeviceSwitch
        fields = ('argument_part_len', 'time_delay', 'time_duration', 'argument_part', 'device', 'mode', 'power_amount',
                  'data_amount', 'request_number')
        read_only_fields = ('argument_part_len',)

    def create(self, validated_data):
        #     # This block is validate a presence of one unique device
        #     # in request.
        #
        device_name = validated_data.pop("device")
        device_mode = validated_data.pop("mode")
        request = validated_data.pop("request")
        dev_list = DeviceSwitch.objects.filter(device__name=device_name, request__number=request['number'])
        if len(dev_list) > 0:
            raise ValidationError("Can not present more than one unique device")
        if "argument_part" in validated_data:
            argument_part = validated_data["argument_part"].split("\n")
            argument_part_len = len(argument_part)
            for line in argument_part:
                if len(line) > 60:
                    raise ValidationError("Every line of the argument part must be shorter than 60 symbols")
        else:
            argument_part_len = 0
        if argument_part_len > 10:
                raise ValidationError("Argument part must be less than 10 lines")
        try:
            device = Device.objects.get(name=device_name)
        except ObjectDoesNotExist:
            raise ValidationError("There is not such device in Database")
        try:
            mode = DeviceMode.objects.get(name=device_mode, device=device)
        except ObjectDoesNotExist:
            raise ValidationError("Such device have not this mode! Please try anouther")
        try:
            request = Request.objects.get(number=request['number'])
        except ObjectDoesNotExist:
            raise ValidationError("Request with this number does not exist yet")
        devswitch = DeviceSwitch(request=request, device=device, mode=mode,
                                 argument_part_len=argument_part_len, **validated_data)
        request.device_amount += 1
        request.save()
        if devswitch.data_amount != mode.data_speed*devswitch.time_duration.total_seconds()/8:
            raise ValidationError("Field data amount not equal to calculated")
        if devswitch.power_amount != mode.power*devswitch.time_duration.total_seconds()/3600:
            raise ValidationError("Field power amount nit equal to calculated")
        devswitch.save()
        return devswitch

class FileNameField(serializers.CharField):
    """
    This class redefined request_file name without full path
    """
    def to_representation(self, obj):
        return os.path.basename(obj)

class RequestSerializer(serializers.ModelSerializer):
    """
    This class collects serialization methods for request creation and attributes from model Request
    """
    request_file = FileNameField(read_only=True)

    class Meta:
        model = Request
        fields = ('number', 'date_start', 'date_end', 'orbit_flag', 'latitude_start',
                  'longitude_left', 'longitude_right', 'device_amount', 'request_file',
                  'creation_date', 'update_date')
        read_only_fields = ('device_amount', 'request_file')

    def create(self, validated_data):
        """
        Redefined create method from Base class
        :param validated_data: data from REST, dictionary with fields in Meta without read_only_fields
        :return: created Request instant
        """
        device_amount = 0
        date_start = date.strftime(validated_data["date_start"], "%d%m%y")
        number = validated_data["number"]
        request_file = 'KNA%(date_start)s%(number)04d.zp' % {
            "date_start": date_start,
            "number": number
        }
        request = Request.objects.create(device_amount=device_amount,
                                         request_file=request_file,
                                         **validated_data)
        return request