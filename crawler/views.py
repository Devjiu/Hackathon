from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import requests


class MIPTCrawler(object):
    def __init__(self, login, password):
        self.login = login
        self.password = password


    def getPersonalInfo(self):
        # session = requests.session()
        credentials = {'USER_LOGIN':self.login, 'USER_PASSWORD':self.password}
        # response = session.post('https://mipt.ru/?login=yes', data=credentials)
        response = HttpResponse('Blah')
        response.set_cookie()
        print(response)

        return response



if __name__ == '__main__':
    crawler = MIPTCrawler('name', '123456')
    crawler.getPersonalInfo()