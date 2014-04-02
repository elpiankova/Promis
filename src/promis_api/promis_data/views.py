# Create your views here.

from django.http import HttpResponse
import json 

def quicklook(request):
    if request.method == 'POST':
        json_request = json.loads(request.POST['json'])
        if json_request.get('type') == 'quicklook':
            pass
        else:
            return HttpResponse('No such type of json requests')
        
        
    