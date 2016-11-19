from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import json


#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    print("FUCK")
    if request.method == 'POST':
        #print(request.body, dict(request.body))
        received_data = json.loads(request.body.decode('utf-8'))
        # return HttpResponse(st)
        print(dict(received_data))
        return HttpResponse(str(received_data))
    return Http404