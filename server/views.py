from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import json


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.


def login(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)

        return HttpResponse(str(received_data))

    return Http404