__author__ = 'len'
import os, sys
#sys.path.append("/home/len/promis/src/promis_api/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "promis_api.settings")

def parse(path):

    path = os.path.normpath(path) # clear reduntant slashes
    (vitok_path,vitok) = os.path.split(path)





if __name__ == "__main__":
    path = ''
    parse(path)