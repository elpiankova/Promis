__author__ = 'len'
import os, sys
import dateutil.parser
import scipy.io
import numpy
import json
import pytz
import glob

sys.path.append("/home/len/promis/src/promis_api/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")

from promis_data.models import Channel, ChannelOption, Parameter, ChannelsHaveParameters
from datetime import timedelta

def potential_parser(path):

    #channels_from_db = Channel.objects.filter(device__satellite__title="Potential")
    path = os.path.normpath(path) # clear redundant slashes

    if os.path.exists(os.path.join(path,'ez/lf/0')):
        #U-low-frequency: 1 Hz
        #choose a channel of db to be loaded with data
        channel_ez_lf = Channel.objects.get(title="U low-frequency")

        telemetry_filename = glob.glob(os.path.join(path,'ez/lf/0/*mv.set'))[0] # got a name of telemetry-file
        telemetry_file = open(telemetry_filename)
        telemetry = telemetry_file.readlines()
        #getting begin_time and number of measurements
        for line in telemetry:
            if 'utc=' in line:
                begin_datetime = dateutil.parser.parse(line.strip().split('utc=')[-1].replace(' ', 'T'))
                print begin_datetime, type(begin_datetime)
            if 'samp=' in line:
                number_of_measurements = int(line.strip().split('samp=')[-1])
        #getting a file with measurements
        measurements_filename = glob.glob(os.path.join(path,'ez/lf/0/*mv.csv'))[0]
        measurements_file = open(measurements_filename)
        measurements_list = measurements_file.readlines()[2:-1]
        #setting a name of measured parameter
        for p in channel_ez_lf.parameters.all():
            if not p.parents.all():
                parameter_name = p.title

        begin_datetime = pytz.utc.localize(begin_datetime)
        #`setting period of measurements, end of session and time of the first measurement
        period = timedelta(seconds=1)# 1/sampling frequency
        end_datetime = begin_datetime + (number_of_measurements - 1)*period
        measurement_datetime = begin_datetime

        yield json.dumps([{"model": "promis_data.session",
                      "fields": {
                                 "time_begin": str(begin_datetime),
                                 "time_end": str(end_datetime)
                                }
                     }])

        for row in measurements_list:
            measurement = float(row.split(',')[0])

            yield json.dumps([{"model": "promis_data.measurementpoint",
                                       "fields": {
                                                  "time": str(measurement_datetime)
                                                 }
                                       }])


            yield json.dumps([{"model": "promis_data.measurement",
                                       "fields": {
                                                  "level_marker": 0,
                                                  "measurement": measurement,
                                                  "parameter": str(parameter_name),
                                                  "channel": [str(channel_ez_lf.title), str(channel_ez_lf.device.title)],
                                                  "measurement_point": [str(measurement_datetime)],
                                                  "session": [str(begin_datetime), str(end_datetime)]
                                                  }
                                       }])
            measurement_datetime += period
    if os.path.exists(os.path.join(path,'ez/hf/00')):
#        U-high-frequncy, 1000 Hz
         channel_ez_hf = Channel.objects.get(title="U High-frequency")



if __name__ == "__main__":
    path = '/home/len/Potential/DECODED/20120405/pdata20120405'
    g = potential_parser(path)
    print next(g)
    print next(g)
    print next(g)
    print next(g)