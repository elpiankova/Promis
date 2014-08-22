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

def potential_parser(path):

    channels_from_db = Channel.objects.filter(device__satellite__title="Potential")
    path = os.path.normpath(path) # clear redundant slashes
    print os.path.exists(os.path.join(path,'ez/lf/0'))
    print
    if os.path.exists(os.path.join(path,'ez/lf/0')):

        telemetry_filename = glob.glob(os.path.join(path,'ez/lf/0/*mv.set'))[0] # get a name of telemetry-file
        telemetry_file = open(telemetry_filename)
        telemetry = telemetry_file.readlines()
        print telemetry
        for line in telemetry:
            if 'utc=' in line:
                time_begin = line.strip().split('utc=')[-1].replace(' ','T')
                print time_begin

if __name__ == "__main__":
    path = '/home/len/Potential/DECODED/20120405/pdata20120405'
    potential_parser(path)