from promis_data.models import *
#from datetime import datetime
import datetime

stime = datetime.datetime.strptime('2011-08-31 21:13:47', '%Y-%m-%d %H:%M:%S')
#delta = datetime.timedelta(0,298,0)
#etime = stime + delta
#ses = Session(time_begin = stime, time_end =etime)
#ses.save()
ses = Session.objects.get(id=1)
param = Parameter.objects.get(title='Voltage')
chann = Channel.objects.get(title = 'U low-frequency')
f = file('/home/elena/workspace/promis/satellite-data/Potential/DECODED/20110831_2/pdata20110831_2/ez/lf/0/lf0105mv.csv', 'r')

lines = f.readlines()
lines.pop(0)
lines.pop(0)

delta = datetime.timedelta(0,1,0)

for line in lines:
    value = float(line.split(',')[0]) * 1000
    mp = MeasurementPoint(time=stime)
    mp.save()
    stime = stime + delta
    m = Measurement(measurement = value, level_marker = 0, parameter = param,
                    channel = chann, measurement_point = mp, session = ses)
    m.save()
    
##         HIGH-frequency  ######### 
chann = Channel.objects.get(title = 'U high-frequency')
f = file('/home/elena/workspace/promis/satellite-data/Potential/DECODED/20110831_2/pdata20110831_2/ez/hf/00/hf0124mv.csv', 'r')

lines = f.readlines()
lines.pop(0)
lines.pop(0)

delta = datetime.timedelta(0,0,0,1)
for line in lines:
    value = float(line.split(',')[0]) * 1000
    mp, created = MeasurementPoint.objects.get_or_create(time=stime)
    #mp.save()
    stime = stime + delta
    m = Measurement(measurement = value, level_marker = 0, parameter = param,
                    channel = chann, measurement_point = mp, session = ses)
    m.save()