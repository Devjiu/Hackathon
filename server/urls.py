from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^getusers/', views.getUsers, name='getusers'),
    url(r'^getlabs/', views.getLabs, name='getlabs'),
    url(r'^getlabusers/', views.getLabUsers, name='getlabusers')
]