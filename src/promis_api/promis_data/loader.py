import os, sys

sys.path.append("/home/elena/workspace/promis/src/promis_api/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")

from parsers import variant_parser
from django.core import serializers
    
def loader(parser, path):
    
    json_generator = parser.variant_parser(path)
    for data in json_generator:
        for deserialized_object in serializers.deserialize("json", data):
            deserialized_object.object.save()


path = '/home/elena/workspace/promis_from_gitlab/satellite-data/Variant/Data_Release1/597'
loader(variant_parser, path)