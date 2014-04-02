'''
Created on Jul 25, 2013

@author: elena piankova
'''
import promis_api.settings as settings
import os
import glob
import datetime # !!!! Only for Time research
import time                   # !!!! Only for Time research

from  filesParsers import setFileParser, parserExchangeFile

satellite_data_path = os.path.join('/'.join(settings.PROJECT_DIR.split('/')[:-2]), 
                                   'satellite-data')

potential_data_path = os.path.join(satellite_data_path, 'Potential/DECODED')

channel_paths = {'ez/lf/0'  : [],
              'ez/hf/00' : [],
              'pd/nkp/0' : [],
              'pd/ekp/00': []}

session_folders = []

print 'Kobevko delta'
delta = datetime.timedelta()
for folder in os.listdir(potential_data_path):
    if folder[:8].isdigit():
        current_path = os.path.join(potential_data_path, folder, 'pdata'+folder)
        session_folders.append(current_path)

#         ''' Parse exchange files from Kobevko program '''
#         exchange_files = glob.glob(os.path.join(current_path, 'tm*.135.txt'))
#  
#         for file_ in exchange_files:
#             (channel_names, channel_units, time_BTS_l, measurements, 
#              time_segmented_l) = parserExchangeFile(os.path.join(current_path, file_))
#             
#             for (time_BST, time_segmented) in zip(time_BTS_l[0], time_segmented_l[0]):
#                 our_time = datetime.datetime(1958, 1, 1, 0, 0, 0) + datetime.timedelta(0, int(time_BST))
#                 kobev_time = datetime.datetime.strptime(time_segmented, "%Y/%m/%d %H:%M:%S") 
#                 if (our_time - kobev_time) != delta:
#                     delta = our_time - kobev_time
#                     print str(our_time), str(kobev_time), delta

           
        ''' Find all path where there are raw data files'''                             
        for channel in channel_paths.keys():
            path = os.path.join(current_path, channel)
            if os.path.exists(path):
                channel_paths[channel].append(path)
                
                #map(set_file_parser, glob.iglob(os.path.join(path, '*mv.set')))

# for session in channel_paths['ez/lf/0']:
#     pass

print 'Shendaruk delta'
delta = datetime.timedelta()
for channel in channel_paths:

    for path in channel_paths[channel]:
        set_files = glob.glob(os.path.join(path, '*mv.set'))
        for set_file in set_files:
            (our_time, shend_time) = setFileParser(set_file)
            if (our_time - shend_time) != delta:
                delta = our_time - shend_time
                print str(our_time), str(shend_time), delta
            

print 'End program'
#DEBUG OUTPUT
# for channel in channel_paths.keys():
#     print(channel_paths[channel])  
#     print(len(channel_paths[channel]))               
# print(len(session_folders))        
#  
# for folder in channel_paths['ez/lf/0'][:1]:
#     for file in os.listdir(folder):
#         pass

