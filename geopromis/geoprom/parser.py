from geoprom.orbit_convertion import PlacePoint
from geoprom.models import Session
from django.contrib.gis.geos import LineString, MultiLineString

new_file = 'geoprom/Adams_pythonFunc_NewCS_dt=10_N=20_ISS.txt' 

def read_file(file_name):
    '''This function read file and create list of points'''
    input = open(file_name)
    data=input.readlines()
    rxryrz_ifr = [[float(i.split()[j].strip()) for i in data[1:]] for j in list(range(1,4))]
    placepoint_list=[]
    for i in range(len(rxryrz_ifr[0])):
        placepoint = PlacePoint(rxryrz_ifr[0][i],rxryrz_ifr[1][i],rxryrz_ifr[2][i])
        placepoint_list.append(placepoint)
    return placepoint_list
    
def session_create(placepoint_list):
    '''This function create session from list of points'''
    border_index = 0
    session_list=[]
    for i in range(len(placepoint_list)-1):
        if (placepoint_list[i].latitude<0 and placepoint_list[i+1].latitude>=0):
            session_list.append(placepoint_list[border_index:i+1])
            border_index=i+1
    session_list.append(placepoint_list[border_index:])
    return session_list

def session_devide(session):
    '''This function create devided session from list of points for map projection'''
    for i in range(len(session)-1):
        if (session[i].longitude*session[i+1].longitude<=-100):
            session = [[j.lonlat for j in session[:i+1]],[k.lonlat for k in session[i+1:]]]
            break
    session_li_bef = LineString(session[0])
    session_li_aft = LineString(session[1])
    session = MultiLineString(session_li_bef,session_li_aft)
    return session

new_file = read_file(new_file)
new_session = session_create(new_file)
for i in range(len(new_session)):
    session_dev = session_devide(new_session[i])
    sat_session = Session(code='gs'+str(i),time_begin='2015-12-20 00:00:00',time_end='2015-12-20 00:00:20',geo_line=session_dev)
    sat_session.save()