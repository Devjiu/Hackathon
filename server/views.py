from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from django.core import serializers
from django.http import JsonResponse

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

        print(response.replace('\"', '\''))
        return JsonResponse(response.replace('\"', '\''), safe=False)