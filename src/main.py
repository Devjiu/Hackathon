import django
from untitled.settings import DATABASES
from django.http import HttpResponse

class superstr():
    def __init__(self, string=''):
        self.string = string

    def get(self):
        return self.string


def hello(request):
    #print("Hello world!")
    return HttpResponse

if __name__ == '__main__':
    print("server")
    print(django.get_version())
    print(DATABASES['default'])