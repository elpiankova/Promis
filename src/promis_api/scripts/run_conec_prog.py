'''
Created on Aug 20, 2013

@author: elena piankova
'''
import promis_api.settings as settings
import os
import glob
from  filesParsers import runKobevkoProg

satellite_data_path = os.path.join('/'.join(settings.PROJECT_DIR.split('/')[:-2]), 
                                   'satellite-data')

potential_data_path = os.path.join(satellite_data_path, 'Potential/DECODED')

for folder in os.listdir(potential_data_path):
    if folder[:8].isdigit():
        current_path = os.path.join(potential_data_path, folder, 'pdata'+folder)
                
        ''' Telemetry files are here. Kobevko program runs here'''
        telemetry_files = glob.glob(os.path.join(current_path, 'tm*.135'))
        telemetry_files.extend(glob.glob(os.path.join(current_path, 'pt*.135')))
        telemetry_files.extend(glob.glob(os.path.join(current_path, 'retransmit/pt*.135')))
        for file_ in telemetry_files:
            runKobevkoProg(os.path.join(current_path, file_), 
                           os.path.join(current_path, file_+'.txt'))
            
print 'End program'