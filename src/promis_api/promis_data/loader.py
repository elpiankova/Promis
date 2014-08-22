import os, sys

sys.path.append("/home/elena/workspace/promis/src/promis_api/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")

from parsers import variant_parser
from django.core import serializers
from django.db.utils import IntegrityError
from datetime import *

sys.stdout = open(str('log' + str(datetime.now())),'w')

def loader(parser, path):
    
    json_generator = parser.variant_parser(path)
    for data in json_generator:
        for deserialized_object in serializers.deserialize("json", data):
            try:
                deserialized_object.object.save()
            except IntegrityError:
                print "%s already exists" % (deserialized_object.object)
            except Exception, e:
                raise Exception(e)
                
path = '/home/len/Variant/Data_Release1/597'
#path = '/home/elena/workspace/Data_Release1_2_session/597/'
loader(variant_parser, path)