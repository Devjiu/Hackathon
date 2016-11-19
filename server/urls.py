from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^welcome/', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
]