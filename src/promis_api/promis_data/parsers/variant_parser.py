__author__ = 'len'
import os, sys
sys.path.append("/home/len/promis/src/promis_api/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")
from promis_data.models import Channel

def parse(path):

    path = os.path.normpath(path) # clear reduntant slashes
    (vitok_path,vitok) = os.path.split(path)
    telemetry_filename = vitok + '.txt'
    telemetry_filename = os.path.join(path, telemetry_filename)

    telemetry_file = open(telemetry_filename, 'r')
    telemetry = telemetry_file.readlines()

    for line in telemetry:
        if 'Sampling frequency' in line:
            metka_freq = telemetry.index(line)
            print 'found'

    Number_of_channels_in_table = channels_from_db.count() - 6
    sampling_frequencies = []
    for i in range(1, Number_of_channels_in_table+1):
        sampling_frequencies += [telemetry[metka_freq+i]]# run through all sampling frequencies and append them to this list
    for freq in sampling_frequencies: # delete all \n and spaces
        sampling_frequencies[sampling_frequencies.index(freq)] = freq.strip()

    for fr in sampling_frequencies:
        if fr == '':
            sampling_frequencies[sampling_frequencies.index(fr)] = None# replace empty lines with None
        else:
            sampling_frequencies[sampling_frequencies.index(fr)] = float(fr)#convert str into float number
    print sampling_frequencies





channels_from_db = Channel.objects.filter(device__satellite__title="Variant")


#print channels_from_db

if __name__ == "__main__":
    path = '/home/len/Variant/Data_Release1/597'
    parse(path)