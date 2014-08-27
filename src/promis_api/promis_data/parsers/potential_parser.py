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

def parse_ez(channel, telemetry_filename, measurements_filename, period):
#    parse data of EZ
#    channel -  db-channel object
#    period - 1/sampling frequency
    telemetry_file = open(telemetry_filename)
    telemetry = telemetry_file.readlines()
    #getting begin_time and number of measurements
    for line in telemetry:
        if 'utc=' in line:
            begin_datetime = dateutil.parser.parse(line.strip().split('utc=')[-1].replace(' ', 'T'))
            #print begin_datetime, type(begin_datetime)
        if 'samp=' in line:
            number_of_measurements = int(line.strip().split('samp=')[-1])
    #getting a file with measurements

    measurements_file = open(measurements_filename)
    measurements_list = measurements_file.readlines()[2:-1]
    #setting a name of measured parameter
    for p in channel.parameters.all():
        if not p.parents.all():
            parameter_name = p.title

    begin_datetime = pytz.utc.localize(begin_datetime)
    #`setting  end of session and time of the first measurement

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
                                              "channel": [str(channel.title), str(channel.device.title)],
                                              "measurement_point": [str(measurement_datetime)],
                                              "session": [str(begin_datetime), str(end_datetime)]
                                              }
                                   }])
        measurement_datetime += period

def parser(path):

    #channels_from_db = Channel.objects.filter(device__satellite__title="Potential")
    path = os.path.normpath(path) # clear redundant slashes


    if os.path.exists(os.path.join(path,'ez/lf/0')):
        #U-low-frequency: 1 Hz
        #choose a channel of db to be loaded with data
        print 'EZ low-frequency channel is to be loaded'
        channel_ez_lf = Channel.objects.get(title="U low-frequency")
        telemetry_filename_lf = glob.glob(os.path.join(path,'ez/lf/0/*mv.set'))[0] # got a name of telemetry-file
        measurements_filename_lf = glob.glob(os.path.join(path,'ez/lf/0/*mv.csv'))[0]
        period_lf = timedelta(seconds=1)# 1/sampling frequency

        data_generator = parse_ez(channel_ez_lf, telemetry_filename_lf, measurements_filename_lf, period_lf)
        for item in data_generator:
            yield item
        print 'EZ low-frequency channel has been loaded'


    if os.path.exists(os.path.join(path,'ez/hf/00')):
#       U-high-frequency, 1000 Hz
        print 'EZ high-frequency channel is to be loaded'

        channel_ez_hf = Channel.objects.get(title="U high-frequency")
        telemetry_filename_hf = glob.glob(os.path.join(path,'ez/hf/00/*mv.set'))[0] # got a name of telemetry-file
        measurements_filename_hf = glob.glob(os.path.join(path,'ez/hf/00/*mv.csv'))[0]
        period_hf = timedelta(milliseconds=1)

        data_gen = parse_ez(channel_ez_hf, telemetry_filename_hf, measurements_filename_hf, period_hf)
        for item in data_gen:
            yield  item
        print 'EZ high-frequency channel has been loaded'





if __name__ == "__main__":
    path = '/home/len/Potential/DECODED/20110905/pdata20110905'
    gen = parser(path)
    print next(gen)
    print next(gen)
    print next(gen)