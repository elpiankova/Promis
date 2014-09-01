__author__ = 'len'
import os, sys
import dateutil.parser
#import scipy.io
#import numpy
#import json
import pytz
import glob
import logging

sys.path.append("/home/len/promis/src/promis_api/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")

from promis_data.models import Channel, ChannelOption, Parameter, ChannelsHaveParameters, Session, MeasurementPoint, Measurement
from datetime import timedelta
from django.db.utils import IntegrityError
from datetime import datetime

logging.basicConfig(level=logging.INFO,  # DEBUG massages will be omitted
                    filename=str(str(datetime.now()) + '.log'),
                    filemode='w',
                    format='%(asctime)s %(lineno)s %(levelname)-8s %(message)s')


def parse_ez(channel, telemetry_filename, measurements_filename, period):
    '''
    parse data of EZ
    channel -  db-channel object
    period - 1/sampling frequency
    '''
    telemetry_file = open(telemetry_filename)
    telemetry = telemetry_file.readlines()
    if not telemetry_file.closed:
        telemetry_file.close()
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
    if not measurements_file.closed:
        telemetry_file.close()
    #setting a name of measured parameter
    for p in channel.parameters.all():
        if not p.parents.all():
            parameter = p

    begin_datetime = pytz.utc.localize(begin_datetime)
    #`setting  end of session and time of the first measurement

    end_datetime = begin_datetime + (number_of_measurements - 1)*period
    measurement_datetime = begin_datetime

    try:
        Session.objects.create(time_begin=begin_datetime, time_end=end_datetime)
        logging.info('Session %s - %s has been created successfully' % (begin_datetime, end_datetime))
    except IntegrityError:
        logging.warning('session %s - %s already exists' % (begin_datetime, end_datetime))
    session = Session.objects.get(time_begin=begin_datetime, time_end=end_datetime)


    count_of_measurements = 0
    if len(measurements_list) < 10000:
        for row in measurements_list:
            measurement = float(row.split(',')[0])

            try:
                MeasurementPoint.objects.create(time=measurement_datetime)
            except IntegrityError:
                logging.warning('Measurement point %s already exists', measurement_datetime)

            meas_point = MeasurementPoint.objects.get(time=measurement_datetime)

            try:
                Measurement.objects.create(level_marker=0,
                                           measurement=measurement,
                                           parameter=parameter,
                                           channel=channel,
                                           measurement_point=meas_point,
                                           session=session)
            except IntegrityError:
                logging.warning('Measurement %s of %s channel already exists', measurement_datetime, channel)

            measurement_datetime += period
            count_of_measurements += 1

        logging.info('%s measurements has been downloaded' % count_of_measurements)

def parser(path):

    #channels_from_db = Channel.objects.filter(device__satellite__title="Potential")
    path = os.path.normpath(path) # clear redundant slashes


    if os.path.exists(os.path.join(path,'ez/lf/0')):
        #U-low-frequency: 1 Hz
        #choose a channel of db to be loaded with data
        logging.info('EZ low-frequency channel is to be loaded')
        channel_ez_lf = Channel.objects.get(title="U low-frequency")
        telemetry_filename_lf = glob.glob(os.path.join(path,'ez/lf/0/*mv.set'))[0] # got a name of telemetry-file
        measurements_filename_lf = glob.glob(os.path.join(path,'ez/lf/0/*mv.csv'))[0]
        period_lf = timedelta(seconds=1)# 1/sampling frequency

        parse_ez(channel_ez_lf, telemetry_filename_lf, measurements_filename_lf, period_lf)
        logging.info('EZ low-frequency channel has been loaded')


    if os.path.exists(os.path.join(path,'ez/hf/00')):
#       U-high-frequency, 1000 Hz
        logging.info('EZ high-frequency channel is to be loaded')

        channel_ez_hf = Channel.objects.get(title="U high-frequency")
        telemetry_filename_hf = glob.glob(os.path.join(path,'ez/hf/00/*mv.set'))[0] # got a name of telemetry-file
        measurements_filename_hf = glob.glob(os.path.join(path,'ez/hf/00/*mv.csv'))[0]
        period_hf = timedelta(milliseconds=1)

        parse_ez(channel_ez_hf, telemetry_filename_hf, measurements_filename_hf, period_hf)
        logging.info('EZ high-frequency channel has been loaded')

if __name__ == "__main__":
    path = '/home/len/Potential/DECODED/20110905/pdata20110905'
    parser(path)
