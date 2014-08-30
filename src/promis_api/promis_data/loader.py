import os
import sys
import logging


sys.path.append("/home/elena/workspace/promis/src/promis_api/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")

from parsers import variant_parser, potential_parser
from django.core import serializers
from django.db.utils import IntegrityError
from datetime import *
import time
import cProfile, pstats, StringIO
import json

pr = cProfile.Profile()
pr.enable()

#sys.stdout = open('logg', 'w')
logging.basicConfig(level=logging.INFO,  # DEBUG massages will be omitted
                    filename=str(str(datetime.now()) + '.log'),
                    filemode='w',
                    format='%(asctime)s %(lineno)s %(levelname)-8s %(message)s')

def loader(parser, path):
    
    json_generator = parser.parser(path)
    for data in json_generator:
        for deserialized_object in serializers.deserialize("json", data):
            try:
                deserialized_object.object.save()
            except IntegrityError:
                logging.debug("%s already exists" % str(deserialized_object.object))  # now omitted
            except Exception, e:
                raise Exception(e)
                
path_variant = '/home/len/Variant/Data_Release1'
#path = '/home/elena/workspace/Data_Release1_2_session/597/'
dirs_variant = []
for folder_name in next(os.walk(path_variant))[1]:
    dirs_variant.append(os.path.join(path_variant, folder_name))
#print dirs

for path in dirs_variant:
    start = time.clock()
    logging.info('%s directory of Variant project is loading' % path)
    loader(variant_parser, path)
    logging.info('%s directory of Variant project has been loaded' % path)
    logging.info('Vitok time: %s' % (time.clock() - start))

path_potential = '/home/len/Potential/DECODED'
dirs_potential = []
for folder in next(os.walk(path_potential))[1]:
    subdir = str(folder + '/pdata' + folder)
    dirs_potential.append(os.path.join(path_potential, subdir))
#print dirs_potential

for path in dirs_potential:
    logging.info('%s directory of Potential project is loading' % path)
    #loader(potential_parser, path)