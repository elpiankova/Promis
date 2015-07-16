from rest_framework import serializers
from .models import Device, DeviceMode, Request, DeviceSwitch

class DeviceModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceMode
        fields = ('name', 'code')

class DeviceSerializer(serializers.ModelSerializer):
    modes = DeviceModeSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ('name', 'code', 'modes')

class DeviceSwitchSerializer(serializers.ModelSerializer):
    device = serializers.StringRelatedField()
    mode = serializers.StringRelatedField()

    class Meta:
        model = DeviceSwitch
        fields = ('argument_part_len', 'time_delay', 'time_duration', 'argument_part', 'device', 'mode')

class RequestSerializer(serializers.ModelSerializer):
    switches = DeviceSwitchSerializer(many=True)

    class Meta:
        model = Request
        fields = ('number', 'date_start', 'date_end', 'orbit_flag', 'latitude_start',
                  'longitude_left', 'longitude_right', 'device_amount', 'request_file',
                  'creation_date', 'update_date', 'switches')

    def create(self, validated_data):
        deviceswitch_data = validated_data.pop('switches')
        request = Request.objects.create(**validated_data)
        for deviceswitch in deviceswitch_data:
            device = Device.objects.get(name=deviceswitch.pop('device'))
            mode = DeviceMode.objects.get(name=deviceswitch.pop("mode"))
            DeviceSwitch.objects.create(request=request, device=device, mode=mode, **deviceswitch)
        return request

