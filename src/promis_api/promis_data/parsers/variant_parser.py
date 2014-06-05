__author__ = 'len'
import os, sys
import dateutil.parser
sys.path.append("/home/len/promis/src/promis_api/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")
from promis_data.models import Channel, ChannelOption

def parse(path):

    path = os.path.normpath(path) # clear redundant slashes
    vitok = os.path.split(path)[1]
    telemetry_filename = vitok + '.txt'
    telemetry_filename = os.path.join(path, telemetry_filename)

    telemetry_file = open(telemetry_filename, 'r')
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
    #print session_interval_strings
    #print begin_datetime, end_datetime

    session_dict = {"model": "promis_data.session",
                    "fields": {
                                "time_begin": begin_datetime,
                                "time_end": end_datetime
                              }
                    }
    #print session_dict

    channels_from_db = Channel.objects.filter(device__satellite__title="Variant")
    number_of_channels_in_table = channels_from_db.count() - 6 # channels E1, E2, E3 of table can denote different electrical fields: E1,E2,E3 or E4,E5,E6 depending on base(E1 or E3)
    sampling_frequencies = []
    for i in range(number_of_channels_in_table):
        # run through all sampling frequencies and append them to this list in float
        # We add None when empty line
        if telemetry[metka_freq+i+1].strip() == '':
            sampling_frequencies.append(None)
        else:
            sampling_frequencies.append(float(telemetry[metka_freq+i+1]))
            
    #print sampling_frequencies

    for channel in channels_from_db:
            options = channel.channeloption_set.get(title='Order number')

            i = int(options.value)
            if sampling_frequencies[i] != None:
                print options
                print sampling_frequencies[i]

    #print ChannelOption.





    #print channels_from_db

if __name__ == "__main__":
#     path = '/home/elena/workspace/promis_from_gitlab/satellite-data/Variant/Data_Release1/597'
    path = '/home/len/Variant/Data_Release1/597'
    parse(path)