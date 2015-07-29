from rest_framework import serializers
from .models import Device, DeviceMode, Request, DeviceSwitch
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.validators import ValidationError
import dateutil.parser, datetime
from ionosat_request.settings import BASE_DIR
import os

class DeviceModeSerializer(serializers.ModelSerializer):
    """
    This class collects serialization methods for device modes and attributes from model DeviceMode
    """
    class Meta:
        model = DeviceMode
        fields = ('name', 'code')


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
    #device = DeviceSerializer()
    device = serializers.SlugRelatedField(slug_field='name', queryset=Device.objects.all())
    mode = serializers.SlugRelatedField(slug_field='name', queryset=DeviceMode.objects.all())

    class Meta:
        model = DeviceSwitch
        fields = ('argument_part_len', 'time_delay', 'time_duration', 'argument_part', 'device', 'mode')
        read_only_fields = ('argument_part_len',)


class FileNameField(serializers.CharField):
    """
    FilePathField is serializated as file name
    """
    def to_representation(self, obj):
        return os.path.basename(obj)

class RequestSerializer(serializers.ModelSerializer):
    """
    This class collects serialization methods for request creation and attributes from model Request
    """
    switches = DeviceSwitchSerializer(many=True)
    request_file = FileNameField()


    class Meta:
        model = Request
        fields = ('number', 'date_start', 'date_end', 'orbit_flag', 'latitude_start',
                  'longitude_left', 'longitude_right', 'device_amount', 'request_file',
                  'creation_date', 'update_date', 'switches')
        read_only_fields = ('device_amount', 'request_file')

    def create(self, validated_data):
        """
        Redefined create method from Base class
        :param validated_data: data from REST, dictionary with fields in Meta without read_only_fields
        :return: created Request instant
        """
        device_switches_data = validated_data.pop('switches')
        list_device_name = []
        for device_switch in device_switches_data:

            # This block is validate a presence of one unique device
            # in request.

            device_name = device_switch["device"]
            if device_name in list_device_name:
                raise ValidationError("Can not present more than one unique device")
            else:
                list_device_name.append(device_name)
            # This block are validate data consistency in argument part

            argument_part = device_switch["argument_part"].split("\r\n")
            if len(argument_part) > 10:
                raise ValidationError("Argument part must be less than 10 lines")
            for line in argument_part:
                if len(line) > 60:
                    raise ValidationError("Every line of the argument part must be shorter than 60 symbols")

        # This block is calculate the amount of devices presented in request form verify argument part length
        # and create objects in data_base with validates fields.

        device_amount = len(device_switches_data)
        request_file = self.create_file(validated_data, device_amount, device_switches_data)
        request = Request.objects.create(device_amount=device_amount, request_file=request_file, **validated_data)
        for device_switch in device_switches_data:
            argument_part_len = len(device_switch["argument_part"].split("\r\n"))
            device = Device.objects.get(name=device_switch.pop('device'))
            mode = DeviceMode.objects.get(name=device_switch.pop('mode'), device=device)
            #data_amount += mode.data_speed*
            DeviceSwitch.objects.create(request=request, device=device, mode=mode, argument_part_len=argument_part_len,
                                        **device_switch)
        return request

    def create_file(self, validated_data, device_amount, device_switches_data):
        """
        Create request file with defined structure
        :param validated_data: data from REST, dictionary with fields in Meta without read_only_fields
        :param device_amount: total amount of devices in one request
        :param device_switches_data: total amount of the switches in one request
        :return: file name of the operational request
        """
        number = validated_data["number"]
        date_start = validated_data["date_start"]
        date_end = validated_data["date_end"]
        date_start = datetime.date.strftime(date_start, "%d%m%y")
        date_end = datetime.date.strftime(date_end, "%d%m%y")
        request_file = 'KNA%(date_start)s%(number)04d.zp' % {"date_start": date_start,
                                                             "number": number}
        # This block writes first line of request file
        file_data = open(os.path.join(BASE_DIR, 'request_files', request_file), 'w')
        first_line = ('KNA %(number)04d %(date_start)s %(date_end)s'
                      ' %(orbit_flag)s %(latitude_start)+04.1f'
                      ' %(longitude_left)05.1f %(longitude_right)05.1f %(device_amount)1d\r\n'
                      % {
                          "number": number,
                          "date_start": date_start,
                          "date_end": date_end,
                          "orbit_flag": validated_data["orbit_flag"],
                          "latitude_start": validated_data["latitude_start"],
                          "longitude_left": validated_data["longitude_left"],
                          "longitude_right": validated_data["longitude_right"],
                          "device_amount": device_amount
                      })
        file_data.write(first_line)

        # This block writes all another lines to request file
        for device_switch in device_switches_data:
            device = Device.objects.get(name=device_switch['device'])
            mode = DeviceMode.objects.get(name=device_switch['mode'], device=device)
            argument_part_len = len(device_switch["argument_part"].split("\r\n"))
            line = ('%(device_code)6s %(mode_code)-8s %(time_delay)06.0f'
                    ' %(time_duration)06.0f %(argument_part_len)02d\r\n'
                    % {
                        "device_code": device.code,
                        "mode_code": mode.code,
                        "time_delay": device_switch["time_delay"].total_seconds(),
                        "time_duration": device_switch["time_duration"].total_seconds(),
                        "argument_part_len": argument_part_len
                    })
            file_data.write(line)

            # This block writes correct end of lines in argument part
            arg_lines = device_switch["argument_part"]
            if arg_lines[-2:] != '\r\n':
                if arg_lines[-1] == '\n':
                    arg_lines = arg_lines.rstrip('\n')
                arg_lines += '\r\n'

            file_data.write(arg_lines)

        file_data.close()
        return request_file
