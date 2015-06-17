import os
import re
import shlex
import subprocess
import datetime
import time

def setFileParser(file_name):
    ''' 
    set_file_parser(string) -> datetime object
    
    Parse .set file from Potential satellite source data and 
    return start time of session  
    '''
    # Check that it's ".set" file 
    extens = os.path.splitext(file_name)[1]
    if extens != '.set':
        raise ValueError("File must be *.set")
    
#     pattern = re.compile(r'''t=([\d]+).*                                              # Read BTS time
#                           utc=([\d]{4}-[\d]{2}-[\d]{2}\ [\d]{2}:[\d]{2}:[\d]{2})      # Read time in "%Y-%m-%d %H:%M:%S" format
#                           ''', flags=re.VERBOSE)
    pattern = re.compile(r't=([\d]+).*utc=([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2})')
    set_file = open(file_name)
    try:
        for line in set_file:
            mo = pattern.search(line)
            if mo is not None:
                (bts_s, utc) = mo.groups()
                break
        
        utc_datetime = datetime.datetime.strptime(utc, "%Y-%m-%d %H:%M:%S")
        bts = datetime.timedelta(0, int(bts_s))
        
        start_time = datetime.datetime(1958, 1, 1, 0, 0, 0)
        session_time_begin = start_time + bts
#         print utc_datetime, delt
 
#         unix_time = time.mktime(utc_datetime.timetuple())
#         delta = time_BTS[j][i] - unix_time
    finally:
        set_file.close()
    
    return session_time_begin, utc_datetime


def runKobevkoProg(source_file, dest_file):
    ''' runKobevkoProg(source_file, dest_file) -> result (True, False)
    
    source_file, dest_file is name of file in string, not File object
    '''
    #try:
    if not os.path.exists(dest_file):
        cmd = './getmi -i ' + source_file + ' -o ' + dest_file
        args = shlex.split(cmd)
        subprocess.Popen(args)
    return
    #except:
    #    return False


def string_merging_4_segmented_time(string1, string2):
    return string1+ " " + string2

def parserExchangeFile(file_name):
    """Function for parsing of exchange file from Conec PI TMI KNAP
    
    parserExchangeFile(file_name) -> (channel_names, channel_units, time_BTS, measurements, time_segmented)
    """
    exchange_file = open(file_name)
    exchange_data = exchange_file.read()
    exchange_file.close()
    data_bloks = exchange_data.split("@")
    if data_bloks == []:
        print 'Data blok is empty'
    # data_bloks[0] -- metadata.
    
    # Metadata parser:
#     print 'First blok is', data_bloks[0] #DEBUG
#     print 'Second blok is', data_bloks[1] #DEBUG
#    print 'First metadata block', data_bloks[0]  # DEBUG
    [descriptive_line, time_creation, session_number, channels] = data_bloks[0].strip().split("\n")
    del data_bloks[0]
    (channel_names, channel_units, time_BTS, measurements, time_segmented) = ([], [], [], [], [])
    # Data parser
    for bloc in data_bloks:
        data = bloc.strip().split()
#        print 'Data bloc', data   #DEBUG
        channel_names.append(data.pop(0))
        channel_units.append(data.pop(0).lstrip("(").rstrip(")"))
        if data != []:
            time_BTS.append(map(int,data[::4]))
            measurements.append(map(float,data[1::4]))
            time_segmented.append(map(string_merging_4_segmented_time, data[2::4], data[3::4]))
    
#    print time_segmented   # DEBUG   
    return (channel_names, channel_units, time_BTS, measurements, time_segmented)
    
#set_file_parser('/home/elena/workspace/promis/satellite-data/Potential/DECODED/20110830/pdata20110830/ez/lf/0/lf0104mv.set')
