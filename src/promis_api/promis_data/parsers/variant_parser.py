__author__ = 'len'
import os, sys
import dateutil.parser
import scipy.io
import numpy
import json

sys.path.append("/home/len/promis/src/promis_api/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")

from promis_data.models import Channel, ChannelOption, Parameter, ChannelsHaveParameters
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta

def parse_telemetry_file(telemetry_file):
    """Parse info file (i.e. 597.txt) with session information.
    Return tuple -> (begin_datetime, end_datetime, base, sampling_frequencies_list)
    """
    telemetry = telemetry_file.read().strip().splitlines()

    for line in telemetry:
        if 'Sampling frequency' in line:
            metka_freq = telemetry.index(line)
        if "EZ1" in line:
            base = "EZ1"
        if "EZ3" in line:
            base = "EZ3"
    session_interval_strings = telemetry[-1].split('(')[0].split()
    begin_datetime = dateutil.parser.parse(session_interval_strings[0])
    end_datetime = dateutil.parser.parse(session_interval_strings[1])
    
    number_of_channels_in_table = Channel.objects.filter(device__satellite__title="Variant").count() - 6 # channels E1, E2, E3 of table can denote different electrical fields: E1,E2,E3 or E4,E5,E6 depending on base(E1 or E3)
    sampling_frequencies = []
    for i in range(number_of_channels_in_table):
        # run through all sampling frequencies and append them to this list in float
        # We add None when empty line
        if telemetry[metka_freq+i+1].strip() == '':
            sampling_frequencies.append(None)
        else:
            sampling_frequencies.append(float(telemetry[metka_freq+i+1]))
    
    return (begin_datetime, end_datetime, base, sampling_frequencies)


def variant_parser(path):
    """Parse Variant source data file that located in path.
    Return generator of json structures in Django serialization form
    """
    path = os.path.normpath(path) # clear redundant slashes
    vitok = os.path.split(path)[1]
    telemetry_file = open(os.path.join(path, vitok + '.txt'), 'r')
    
    (begin_datetime, 
     end_datetime, 
     base, 
     sampling_frequencies) = parse_telemetry_file(telemetry_file)
    
    #print begin_datetime, end_datetime

    yield json.dumps([{"model": "promis_data.session",
                      "fields": {
                                 "time_begin": str(begin_datetime),
                                 "time_end": str(end_datetime)
                                }
                     }])

    channels_from_db = Channel.objects.filter(device__satellite__title="Variant")

    for channel in channels_from_db:


        channel.base_sensor = 1 # this variable should exist and != None, the unity was the first choice
        try: # check if option 'Base sensor' exists for current channel
            channel.base_sensor = channel.channeloption_set.get(title='Base sensor').value # this can arise an exception
            #print ' the base sensor is ' + str(channel.base_sensor)
            if channel.base_sensor != base:
                channel.base_sensor = None
        except ObjectDoesNotExist:
            pass
        
        channel.order_number = channel.channeloption_set.get(title='Order number').value
        channel.filename = channel.channeloption_set.get(title='Filename').value

        for p in channel.parameters.all():
            if not p.parents.all():
                parameter_name = p.title


        if sampling_frequencies[int(channel.order_number)] != None and channel.base_sensor != None:
        #                                                              to skip all channels with wrong base sensor
            print channel.filename

            if str(channel.filename) + '.mat' in os.listdir(path): # mat-files should be checked first because ..
            # 1) text files have no extension, 2) every mat-file has file with the same name and without extension

                measurement_file_dict = scipy.io.loadmat(os.path.join(path, str(channel.filename)) + '.mat')
                for key in measurement_file_dict:# executes search of data and saves it in numpy.ndarray type
                    if type(measurement_file_dict[key]) == numpy.ndarray:
                        measurement_file_column = measurement_file_dict[key]
                measurement_row = measurement_file_column.transpose()[0]
            elif str(channel.filename) in os.listdir(path):
                measurement_file = open(os.path.join(path, str(channel.filename)))
                measurement_row = numpy.fromfile(measurement_file, dtype=numpy.float64, sep=' ')
            else:
                print 'No file "' + str(channel.filename) + '" found'
            print type(measurement_row)

            period_microsec =  timedelta(microseconds=1/sampling_frequencies[int(channel.order_number)]*10**6)
            measurement_datetime = begin_datetime

            for measurement in measurement_row:

                if measurement != 0: #


                    yield json.dumps([{"model": "promis_data.measurement",
                          "fields": {
                                    "level_marker": 0,
                                    "measurement": measurement,
                                    "parameter": str(parameter_name),
                                    "channel": [str(channel.title), str(channel.device.title)],
                                    "measurement_point": [str(measurement_datetime)],
                                    "session": [str(begin_datetime), str(end_datetime)]
                                    }
                         }])

                    measurement_datetime += period_microsec
                    pass




#print ChannelOption.




#print channels_from_db

if __name__ == "__main__":
#     path = '/home/elena/workspace/promis_from_gitlab/satellite-data/Variant/Data_Release1/597'
    path = '/home/len/Variant/Data_Release1/597'
    gen = variant_parser(path)
    print next(gen)
    print next(gen)
    print next(gen)



    
