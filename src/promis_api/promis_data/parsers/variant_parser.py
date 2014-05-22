__author__ = 'len'
import os, sys
sys.path.append("/home/len/promis/src/promis_api/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")
from promis_data.models import Channel

def parse(path):

    path = os.path.normpath(path) # clear reduntant slashes
    (vitok_path,vitok) = os.path.split(path)
    telemetry_file = vitok + '.txt'
    telemetry_file = os.path.join(path, telemetry_file)

channels_from_db = Channel.objects.filter(device__satellite__title="Variant")
print channels_from_db

if __name__ == "__main__":
    path = ''
    parse(path)
