__author__ = 'len'
import os, sys
import dateutil.parser
import scipy.io
import numpy
import json
from promis_data.models import Channel, ChannelOption

sys.path.append("/home/len/promis/src/promis_api/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")


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


def parse(path):
    
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
    #print session_dict

    channels_from_db = Channel.objects.filter(device__satellite__title="Variant")

    for channel in channels_from_db:
        order_number = channel.channeloption_set.get(title='Order number')
        filename = channel.channeloption_set.get(title='Filename')

        if sampling_frequencies[int(order_number.value)] != None:
            #print options_order_number
            print filename.value
            #print sampling_frequencies[i]
            if str(filename.value) + '.mat' in os.listdir(path): # mat-files should be checked first because ..
            # 1) text files have no extension, 2) every mat-file has file with the same name and without extension

                measurement_file_dict = scipy.io.loadmat(os.path.join(path, str(filename.value)) + '.mat')
                for key in measurement_file_dict:# executes search of data and saves it in numpy.ndarray type !!!
                    if type(measurement_file_dict[key]) == numpy.ndarray:
                        measurement_file = measurement_file_dict[key]
                        print type(measurement_file)# type 'numpy.ndarray'
            elif str(filename.value) in os.listdir(path):
                measurement_file = open(os.path.join(path, str(filename.value)))
            else:
                print 'No file "' + str(filename.value) + '" found'


    #print ChannelOption.




    #print channels_from_db

if __name__ == "__main__":
#     path = '/home/elena/workspace/promis_from_gitlab/satellite-data/Variant/Data_Release1/597'
    path = '/home/len/Variant/Data_Release1/597'
    parse(path)