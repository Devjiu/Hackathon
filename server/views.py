from itertools import chain

from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from django.core import serializers
from django.http import JsonResponse
from operator import attrgetter

# from django.utils import simplejson

import json
import server.models as mod


methodmap = { '0' : 'lab',
              '1' : 'project',
              '2' : 'event'}


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
            instance['skills'] = _getUserSkills(instance['member_id'])

            """ Add interests """
            instance['interests'] = _getUserInterests(instance['member_id'])

        return JsonResponse(data, safe=False)
    return Http404

# def searchLabs(request):
#
# def searchProjects(request):

def searchEvents(request):
    search_word = list(request.GET)[0]
    print(search_word)
    qs1 = mod.Event.objects.filter(name__icontains=search_word)
    qs2 = mod.Event.objects.filter(description__icontains=search_word)
    qs3 = mod.EventTechnologies.objects.filter( Q(skill1__icontains=search_word) |
                                                Q(skill2__icontains=search_word) |
                                                Q(skill3__icontains=search_word) |
                                                Q(skill4__icontains=search_word) |
                                                Q(skill5__icontains=search_word))
    result_list = sorted(
        chain(qs1, qs2, qs3),
        key=attrgetter('project_id'))
    print(result_list)
    response = serializers.serialize("json", result_list, fields=('project_id'))
    users = json.loads(response)
    keyset = set()
    if len(users):
        result = [x['fields'] for x in users][0]
        keyset.add(result['project_id'])
    result = []
    for key in keyset:
        info = _getEventName(key)
        #print('Name:',_getEventName(key))
        print('Info: ',info)
        info['skills']= _getEventTech(key)
        print(info)
        #info['description'] = _getEventName(key)
        result.append(info)
    print(result)
    return JsonResponse(result, safe=False)

def searchUser(request):
    req = dict(request.GET)
    key = list(req)[0]
    print(key)
    qs1 = mod.Member.objects.filter(first_name__icontains = key)
    qs2 = mod.Member.objects.filter(last_name__icontains = key)
    qs3 = mod.MemberInterest.objects.filter(Q(interest1__icontains=key) |
                                      Q(interest2__icontains=key) |
                                      Q(interest3__icontains=key) |
                                      Q(interest4__icontains=key) |
                                      Q(interest5__icontains=key))
    qs4 = mod.MemberSkills.objects.filter(Q(skill1__icontains=key) |
                                    Q(skill2__icontains=key) |
                                    Q(skill3__icontains=key) |
                                    Q(skill4__icontains=key) |
                                    Q(skill5__icontains=key))
    qs5 = mod.MemberAchievements.objects.filter(Q(achievement1__icontains=key) |
                                            Q(achievement2__icontains=key) |
                                            Q(achievement3__icontains=key) |
                                            Q(achievement4__icontains=key) |
                                            Q(achievement5__icontains=key))

    result_list = sorted(
        chain(qs1, qs2, qs3, qs4, qs5),
        key=attrgetter('member_id'))
    response = serializers.serialize("json", result_list, fields=('member_id'))
    users = json.loads(response)
    print(users)
    keyset = set()
    if len(users):
        result = [x['fields'] for x in users][0]
        print("res:",result['member_id'])
        keyset.add(result['member_id'])
    print(keyset)
    result = []
    for key in keyset:
        info = _getUserInfo(key)
        info['skills'] = _getUserSkills(key)
        info['interests'] = _getUserInterests(key)
        result.append(info)
    print(result)
    return JsonResponse(result, safe=False)

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


""" USER SECTION """
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
        # result.pop('member_id')

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

""" PROJECT SECTION """
def _getProjectInfo(project_id):
    """ Returns project info """
    print("---------------------------")

    print("getting user interests id = ", project_id)
    info = mod.Project.objects.filter(project_id=int(project_id))
    info = serializers.serialize('json', info,
                                      fields=(
                                      'project_id', 'name', 'description', 'is_lab'))
    info = json.loads(info)
    result = []
    if len(info):
        result = [x['fields'] for x in info][0]
        print(result)
        to_delete = []
        for key in result:
            if result[key] == '' or key == 'project_id':
                to_delete.append(key)

        for key in to_delete:
            result.pop(key)

    print("result : ", result)
    print("---------------------------")
    return result

def _getProjectSkills(project_id):
    """ Returns project skills """
    print("---------------------------")

    print("getting user interests id = ", project_id)
    skills = mod.ProjectSkills.objects.filter(project_id=int(project_id))
    skills = serializers.serialize('json', skills,
                                      fields=(
                                      'project_id', 'skill1','skill2', 'skill3', 'skill4', 'skill5'))
    skills = json.loads(skills)
    result = []
    if len(skills):
        result = [x['fields'] for x in skills][0]
        print(result)
        to_delete = []
        for key in result:
            if result[key] == '' or key == 'project_id':
                to_delete.append(key)

        for key in to_delete:
            result.pop(key)

    print("result : ", result)
    print("---------------------------")
    return result

def _getProjectInterests(project_id):
    """ Returns project Interests """
    print("---------------------------")

    print("getting user interests id = ", project_id)
    interests = mod.ProjectInterest.objects.filter(project_id=int(project_id))
    interests = serializers.serialize('json', interests,
                                      fields=(
                                      'project_id', 'interest1', 'interest2', 'interest3', 'interest4', 'interest5'))
    interests = json.loads(interests)
    result = []
    if len(interests):
        result = [x['fields'] for x in interests][0]
        print(result)
        to_delete = []
        for key in result:
            if result[key] == '' or key == 'project_id':
                to_delete.append(key)

        for key in to_delete:
            result.pop(key)

    print("result : ", result)
    print("---------------------------")
    return result

def _getEventInfo(project_id):
    print("---------------------------")

    print("getting event projects id = ", project_id)
    info = mod.EventTechnologies.objects.filter(project_id=int(project_id))
    print("getting event projects info = ", info)
    info = serializers.serialize('json', info,
                                 fields=(
                                     'project_id', 'name', 'description', 'is_lab',
                                     'skill1', 'skill2', 'skill3', 'skill4', 'skill5'))
    info = json.loads(info)
    result = []
    if len(info):
        result = [x['fields'] for x in info][0]
        print(result)
        to_delete = []
        for key in result:
            if result[key] == '' or key == 'project_id':
                to_delete.append(key)

        for key in to_delete:
            result.pop(key)

    print("result : ", result)
    print("---------------------------")
    return result

def _getEventName(project_id):
    print("---------------------------")

    print("getting event projects id = ", project_id)
    info = mod.Event.objects.filter(project_id=int(project_id))
    info = serializers.serialize('json', info,
                                 fields=(
                                     'project_id', 'name', 'description', 'is_lab',
                                     'skills'))
    info = json.loads(info)
    result = []
    if len(info):
        result = [x['fields'] for x in info][0]
        print(result)
        to_delete = []
        for key in result:
            if result[key] == '' or key == 'project_id':
                to_delete.append(key)

        for key in to_delete:
            result.pop(key)

    print("result : ", result)
    print("---------------------------")
    return result

def _getEventTech(project_id):
    """ Returns project info """
    print("---------------------------")

    print("getting event technologies id = ", project_id)
    tech = mod.EventTechnologies.objects.filter(project_id=int(project_id))
    tech = serializers.serialize('json', tech,
                                 fields=(
                                     'project_id', 'skill1', 'skill2', 'skill3', 'skill4', 'skill5'))
    tech = json.loads(tech)
    result = []
    if len(tech):
        result = [x['fields'] for x in tech][0]
        print(result)
        to_delete = []
        for key in result:
            if result[key] == '' or key == 'project_id':
                to_delete.append(key)

        for key in to_delete:
            result.pop(key)

    print("result : ", result)
    print("---------------------------")
    return result

""" GETTERS """
def getLabUsers(request):
    if request.method == 'GET':
        req = dict(request.GET)

        users = mod.Crossings.objects.filter(project_id=int(req['id'][0]))
        users = serializers.serialize('json',users, fields=('project_id', 'member_id'))
        users = json.loads(users)

        result = []
        if len(users):
            users = [x['fields'] for x in users]

            for user in users:
                info = _getUserInfo(user['member_id'])
                info['skills'] = _getUserSkills(user['member_id'])
                info['interests'] = _getUserInterests(user['member_id'])
                result.append(info)

        return JsonResponse(result, safe=False)
    return Http404

def getProjects(request):
    if request.method == 'GET':
        response = serializers.serialize('json',
                                         mod.Project.objects.all(),
                                         fields=('name', 'description', 'is_lab', 'project_id'))
        labs = json.loads(response)
        print(labs)
        labs = [x['fields'] for x in labs]
        result = []
        for lab in labs:
            if not lab['is_lab']:
                result.append(lab)

        for instance in labs:
            """ Add skills """
            instance['skills'] = _getProjectSkills(instance['project_id'])

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

def getEvents(request):
    if request.method == 'GET':
        info = mod.Event.objects.all()
        info = serializers.serialize('json', info,
                                     fields=(
                                         'project_id', 'name', 'description', 'time'))
        info = json.loads(info)
        result = []
        if len(info):
            result = [x['fields'] for x in info]

        for instance in result:
            tech = _getEventTech(instance['project_id'])
            instance['skills'] = tech

        return JsonResponse(result, safe=False)
    return Http404

def getEventUsers(request):
    if request.method == 'GET':
        req = dict(request.GET)

        users = mod.CrossEvent.objects.filter(project_id=int(req['id'][0]))
        users = serializers.serialize('json',users, fields=('project_id', 'member_id'))
        users = json.loads(users)
        print(users)
        result = []
        if len(users):
            users = [x['fields'] for x in users]

            for user in users:
                info = _getUserInfo(user['member_id'])
                info['skills'] = _getUserSkills(user['member_id'])
                info['interests'] = _getUserInterests(user['member_id'])
                result.append(info)

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


def acceptLab(request):
    if request.method == 'GET':
        params = dict(request.GET)
        print(int(params['accept'][0]))
        if int(params['type'][0]) == 2:
            if int(params['accept'][0]) == 1:
                print("here")
                try :
                    p = mod.CrossEvent.objects.create(project_id=int(params['lab'][0]),
                                                member_id=int(params['user'][0]))
                except:
                    print("Object exists")

                print("Added")
            else:
                try:
                    p = mod.CrossEvent.objects.get(project_id=int(params['lab'][0]),
                                                   member_id=int(params['user'][0])).delete()
                    print("Deleted")

                except mod.CrossEvent.DoesNotExist:
                    print("No such value")
            return JsonResponse({"OK": 1})
        elif int(params['type'][0]) == 1 or int(params['type'][0]) == 0:
            if int(params['accept'][0]) == 1:
                try:
                    p = mod.Crossings.objects.create(project_id=int(params['lab'][0]),
                                                  member_id=int(params['user'][0]))
                except:
                    print("Object exists")

                print("Added")
            else:
                try:
                    p = mod.Crossings.objects.get(project_id=int(params['lab'][0]),
                                                   member_id=int(params['user'][0])).delete()
                    print("Deleted")

                except mod.CrossEvent.DoesNotExist:
                    print("No such value")
            return JsonResponse({"OK": 1})
    return Http404