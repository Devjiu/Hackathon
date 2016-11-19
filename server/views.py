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
        response = serializers.serialize('json',
                                         mod.Member.objects.all(),
                                         fields=('first_name', 'last_name', 'member_id'))

        d = json.loads(response)
        # print(d)
        # print(d)
        # print(d)
        data = [x['fields'] for x in d]
        print("data : ", data)
        for instance in data:
            # print("instance = ", instance)
            """ Add skills """
            resp = serializers.serialize('json',
                                           mod.MemberSkills.objects.all(),
                                           fields=('skill1','skill2', 'skill3', 'skill4', 'skill5', 'member_id'))
            skills = json.loads(resp)
            skills = [x['fields'] for x in skills][0]
            print(skills)

            if instance['member_id'] == skills['member_id']:
                # for skill in skills:
                #     instance[skill] = skills[skill]
                to_delete = []
                for key in skills:
                    if skills[key] == '' or key == 'member_id':
                        to_delete.append(key)

                for key in to_delete:
                    skills.pop(key)
                instance['skills'] = skills

            """ Add interests """

            resp = serializers.serialize('json',
                                         mod.MemberInterest.objects.all(),
                                         fields=('interest1', 'interest2', 'interest3', 'interest4', 'interest5', 'member_id'))
            interests = json.loads(resp)
            interests = [x['fields'] for x in interests][0]
            print("interests : ", interests)

            if instance['member_id'] == interests['member_id']:
                # for interest in interests:
                #     instance[interest] = interests[interest]
                to_delete = []
                for key in interests:
                    if interests[key] == '' or key == 'member_id':
                        to_delete.append(key)
                # interests.pop('member_id')
                for key in to_delete:
                    interests.pop(key)
                instance['interests'] = interests

        # print(data)
        # print(dict(data))
        return JsonResponse(data, safe=False)
        # return HttpResponse(simplejson.dumps(response.replace('\"', '\'')), mimetype='application/json')

