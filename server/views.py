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
    """ Returns all users info """
    if request.method == 'GET':
        response = serializers.serialize('json',
                                         mod.Member.objects.all(),
                                         fields=('first_name', 'last_name', 'member_id', 'comment', 'status'))

        d = json.loads(response)

        data = [x['fields'] for x in d]
        print("data : ", data)
        for instance in data:

            """ Add skills """
            resp = serializers.serialize('json',
                                           mod.MemberSkills.objects.all(),
                                           fields=('skill1','skill2', 'skill3', 'skill4', 'skill5', 'member_id'))
            skills = json.loads(resp)
            if len(skills):
                skills = [x['fields'] for x in skills][0]
                print(skills)

                if instance['member_id'] == skills['member_id']:

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
            if len(interests):
                interests = [x['fields'] for x in interests][0]
                print("interests : ", interests)

                if instance['member_id'] == interests['member_id']:

                    to_delete = []
                    for key in interests:
                        if interests[key] == '' or key == 'member_id':
                            to_delete.append(key)

                    for key in to_delete:
                        interests.pop(key)
                    instance['interests'] = interests

        return JsonResponse(data, safe=False)
    return Http404


def getLabs(request):
    if request.method == 'GET':
        response = serializers.serialize('json',
                                         mod.Project.objects.all(),
                                         fields=('name', 'description', 'is_lab', 'project_id'))
        labs = json.loads(response)
        print(labs)
        labs = [x['fields'] for x in labs]
        result = []
        for lab in labs:
            if lab['is_lab']:
                result.append(lab)

        for instance in labs:
            """ Add skills """
            resp = serializers.serialize('json',
                                         mod.ProjectSkills.objects.all(),
                                         fields=('skill1','skill2', 'skill3', 'skill4', 'skill5', 'project_id'))
            skills = json.loads(resp)
            if len(skills):
                skills = [x['fields'] for x in skills][0]
                if instance['project_id'] == skills['project_id']:

                    to_delete = []
                    for key in skills:
                        if skills[key] == '' or key == 'project_id':
                            to_delete.append(key)

                    for key in to_delete:
                        skills.pop(key)
                instance['skills'] = skills

            """ Add interests """

            resp = serializers.serialize('json',
                                         mod.ProjectInterest.objects.all(),
                                         fields=(
                                         'interest1', 'interest2', 'interest3', 'interest4', 'interest5', 'project_id'))
            interests = json.loads(resp)
            if len(interests):
                interests = [x['fields'] for x in interests][0]
                print("interests : ", interests)

                if instance['project_id'] == interests['project_id']:

                    to_delete = []
                    for key in interests:
                        if interests[key] == '' or key == 'project_id':
                            to_delete.append(key)

                    for key in to_delete:
                        interests.pop(key)
                    instance['interests'] = interests

        return JsonResponse(result, safe=False)
    return Http404


def _getUserInfo(user_id):
    """ Returns dict of member """
    print("---------------------------")

    print("getting user info id = ", user_id)
    users = mod.Member.objects.filter(member_id=int(user_id))
    users = serializers.serialize('json', users,
                                   fields=('member_id', 'first_name', 'last_name', 'status', 'comment'))
    users = json.loads(users)
    result = []
    if len(users):
        result = [x['fields'] for x in users][0]
        print(result)
        to_delete = []
        for key in result:
            if result[key] == '' or key == 'member_id':
                to_delete.append(key)

        for key in to_delete:
            result.pop(key)

    print("result : ", result)
    print("---------------------------")
    return result


def _getUserSkills(user_id):
    """ Returns dict of skills """
    print("---------------------------")

    print("gettin user skills id = ", user_id)
    skills = mod.MemberSkills.objects.filter(member_id=int(user_id))
    skills = serializers.serialize('json', skills, fields=('member_id', 'skill1','skill2', 'skill3', 'skill4', 'skill5'))
    skills = json.loads(skills)
    result = []
    if len(skills):
        result=  [x['fields'] for x in skills][0]
        print(result)
        to_delete = []
        for key in result:
            if result[key] == '' or key == 'member_id':
                to_delete.append(key)

        for key in to_delete:
            result.pop(key)

    print("result : ", result)
    print("---------------------------")
    return result

def _getUserInterests(user_id):
    """ Returns user interests """
    print("---------------------------")

    print("getting user interests id = ", user_id)
    interests = mod.MemberInterest.objects.filter(member_id=int(user_id))
    interests = serializers.serialize('json', interests,
                                   fields=('member_id', 'interest1', 'interest2', 'interest3', 'interest4', 'interest5'))
    interests = json.loads(interests)
    result = dict()
    if len(interests):
        result = [x['fields'] for x in interests][0]
        print(result)
        to_delete = []
        for key in result:
            if result[key] == '' or key == 'member_id':
                to_delete.append(key)

        for key in to_delete:
            result.pop(key)

    print("result : ", result)
    print("---------------------------")
    return result



def getLabUsers(request):
    if request.method == 'GET':
        req = dict(request.GET)
        print(req)
        users = mod.Crossings.objects.filter(project_id=int(req['id'][0]))
        users = serializers.serialize('json',users, fields=('project_id', 'member_id'))
        users = json.loads(users)
        print(users[0])
        result = dict()
        if len(users):
            users = [x['fields'] for x in users]

            print(users)
            for user in users:
                # tmp = mod.Member.objects.filter(member_id=user['member_id'])
                # skills = mod.MemberSkills.objects.filter(member_id=user['member_id'])
                # interests = mod.MemberInterest.objects.filter(member_id=user['member_id'])
                # print(tmp, skills, interests)
                info = _getUserInfo(user['member_id'])
                info['skills'] = _getUserSkills(user['member_id'])
                info['interests'] = _getUserInterests(user['member_id'])
                result = info

        return JsonResponse(result, safe=False)
    return Http404


def compareDicts(dict_a, dict_b):
    keys_a = set(dict_a.keys())
    keys_b = set(dict_b.keys())
    intersection = keys_a & keys_b
    similar = 0
    for key in intersection:
        if dict_a[key] == dict_b[key]:
            similar += 1
    return similar


def dictInclude(dict_bigger, dict_smaller):
    keys_big = set(dict_bigger.keys())
    keys_smal= set(dict_smaller.keys())
    key_match = keys_smal.issubset(keys_big)
    if not key_match:
        return False
    for key in keys_smal:
        if dict_smaller[key] != dict_bigger[key]:
            return False

    return True

