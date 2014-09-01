__author__ = 'len'
import os, sys
import dateutil.parser
import scipy.io
import numpy
import pytz
import logging
import cProfile, pstats, StringIO

pr = cProfile.Profile()

sys.path.append("/home/len/promis/src/promis_api/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")

from promis_data.models import Channel, ChannelOption, Parameter, ChannelsHaveParameters, Session, MeasurementPoint, Measurement
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta,datetime
from django.db.utils import IntegrityError

#logging.basicConfig(level=logging.INFO,  # DEBUG massages will be omitted
#                    filename=str(str(datetime.now()) + '.log'),
#                    filemode='w',
#                    format='%(asctime)s %(lineno)s %(levelname)-8s %(message)s')

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

    number_of_channels_in_table = Channel.objects.filter(device__satellite__title="Variant").count() - 6  # channels E1, E2, E3 of table can denote different electrical fields: E1,E2,E3 or E4,E5,E6 depending on base(E1 or E3)
    sampling_frequencies = []
    for i in range(number_of_channels_in_table):
        # run through all sampling frequencies and append them to this list in float
        # We add None when empty line
        if telemetry[metka_freq+i+1].strip() == '':
            sampling_frequencies.append(None)
        else:
            sampling_frequencies.append(float(telemetry[metka_freq+i+1]))

    return (begin_datetime, end_datetime, base, sampling_frequencies)


def parser(path):
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

    if not telemetry_file.closed:
        telemetry_file.close()

    #print begin_datetime, end_datetime

    begin_datetime = pytz.utc.localize(begin_datetime) - timedelta(hours=3)
    end_datetime = pytz.utc.localize(end_datetime) - timedelta(hours=3)
    try:
        Session.objects.create(time_begin=begin_datetime, time_end=end_datetime)
        logging.info('Session %s - %s has been created successfully' % (begin_datetime, end_datetime))
    except IntegrityError:
        logging.warning('session %s - %s already exists' % (begin_datetime, end_datetime))
    session = Session.objects.get(time_begin=begin_datetime, time_end=end_datetime)

    channels_from_db = Channel.objects.filter(device__satellite__title="Variant")

    for channel in channels_from_db:

        channel.base_sensor = 1  # this variable should exist and != None, the unity was the first choice
        try: # check if option 'Base sensor' exists for current channel
            channel.base_sensor = channel.channeloption_set.get(title='Base sensor').value  # this can arise an exception
            #print ' the base sensor is ' + str(channel.base_sensor)
            if channel.base_sensor != base:
                channel.base_sensor = None
        except ObjectDoesNotExist:
            pass
        print channel.title
        channel.order_number = channel.channeloption_set.get(title='Order number').value
        channel.filename = channel.channeloption_set.get(title='Filename').value
        try:
            channel.conv_factor = 1/float(channel.channeloption_set.get(title='Conversion factor').value)
        except ChannelOption.DoesNotExist:
            channel.conv_factor = 1

        for p in channel.parameters.all():
            if not p.parents.all():
                parameter = p
        count = 0  # for counting measurements within one channel
        measurement_row = []  #
        if sampling_frequencies[int(channel.order_number)] is not None and channel.base_sensor is not None:
        #                                                              to skip all channels with wrong base sensor
            if str(channel.filename) + '.mat' in os.listdir(path):  # mat-files should be checked first because ..
            # 1) text files have no extension, 2) every mat-file has file with the same name and without extension
                measurement_file_dict = scipy.io.loadmat(os.path.join(path, str(channel.filename)) + '.mat')
                for key in measurement_file_dict:  # executes search of data and saves it in numpy.ndarray type
                    if type(measurement_file_dict[key]) == numpy.ndarray:
                        measurement_file_column = measurement_file_dict[key]
                measurement_row = measurement_file_column.transpose()[0]
            elif str(channel.filename) in os.listdir(path):
                measurement_file = open(os.path.join(path, str(channel.filename)))
                measurement_row = numpy.fromfile(measurement_file, dtype=numpy.float64, sep=' ')
                if not measurement_file.closed:
                    measurement_file.close()
            else:
                logging.warning('No file %s found' % channel.filename)
            #print type(measurement_file_dict)

            logging.info('%s channel is to be loaded with %s measurements' % (channel.filename, len(measurement_row)))

            period_microsec = timedelta(microseconds=1/sampling_frequencies[int(channel.order_number)]*10**6)
            measurement_datetime = begin_datetime
            if len(measurement_row) < 10000:
                for measurement in measurement_row:
                    #pr.enable()
                    if measurement != 0:

                        measurement *= channel.conv_factor
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
                        measurement_datetime += period_microsec
                        count += 1
                    #pr.disable()
                    #s = StringIO.StringIO()
                    #sortby = 'cumulative'
                    #ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
                    #ps.print_stats()
                    #logging.info('%s' % s.getvalue())

        logging.info('%s channel has been loaded with %s measurements', channel.filename, count)


#print channels_from_db

if __name__ == "__main__":
    import timeit
    path = '/home/len/Variant/Data_Release1/1056'
#    path = '/home/elena/workspace/promis_from_gitlab/satellite-data/Variant/Data_Release1/597'
    parser(path)

    print timeit.timeit('parser("/home/len/Variant/Data_Release1/1056")', 'from __main__ import parser')