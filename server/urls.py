from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^getusers/', views.getUsers, name='getusers'),
    url(r'^getlabs/', views.getLabs, name='getlabs'),
    url(r'^getprojects/', views.getProjects, name='getprojects'),
    url(r'^getevents/', views.getEvents, name='getevents'),
    url(r'^getlabusers/', views.getLabUsers, name='getlabusers'),
    url(r'^geteventusers/', views.getEventUsers, name='geteventusers'),
    url(r'^getprojectusers/', views.getProjectUsers, name='getprojectusers'),
    url(r'^searchusers/', views.searchUser, name='searchusers'),
    url(r'^acceptlab/', views.acceptLab, name='acceptlab'),
    url(r'^searchevents/', views.searchEvents, name='searchuevents'),
    url(r'^searchlabs/', views.searchLabs, name='searchlabs'),
    url(r'^searchprojects/', views.searchProjects, name='searchprojects'),
    url(r'^addaccounts/', views.add10accounts, name='add10accounts')
]
