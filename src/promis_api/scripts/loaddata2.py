from promis_data.models import Session, Parameter, Channel, Measurement, MeasurementPoint
# from promis_api.settings import PROJECT_DIR 

import datetime

#file_name = 

stime = datetime.datetime.strptime('2011-09-05 18:08:16', '%Y-%m-%d %H:%M:%S')
delta = datetime.timedelta(0,297,0)
etime = stime + delta
ses = Session(time_begin = stime, time_end =etime)
ses.save()
#ses = Session.objects.get(id=1)
param = Parameter.objects.get(title='Voltage')
chann = Channel.objects.get(title = 'U low-frequency')
f = file('/home/elena/workspace/promis/satellite-data/Potential/DECODED/20110905/pdata20110905/ez/lf/0/lf0107mv.csv', 'r')

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
    