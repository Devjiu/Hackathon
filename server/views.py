from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from django.core import serializers
from django.http import JsonResponse

# from django.utils import simplejson

import json
import server.models as mod

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")



def login(request):
    if request.method == 'POST':
        #print(request.body, dict(request.body))
        received_data = json.loads(request.body.decode('utf-8'))
        # return HttpResponse(st)
        print(dict(received_data))
        return HttpResponse(str(received_data))

    return Http404

def getUsers(request):
    if request.method == 'GET':
        response = serializers.serialize('json', mod.Member.objects.all(), fields=('first_name', 'last_name'))

        d = json.loads(response)

        # print(d)
        data = [x['fields'] for x in d]
        # print(data)
        # print(dict(data))
        return JsonResponse(data, safe=False)
        # return HttpResponse(simplejson.dumps(response.replace('\"', '\'')), mimetype='application/json')

