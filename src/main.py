import django
from untitled.settings import DATABASES

class superstr():
    def __init__(self, string=''):
        self.string = string

    def get(self):
        return self.string
        

def hello(*args, **kwargs):
    #print("Hello world!")
    return '<h>Hello</h>'

if __name__ == '__main__':
    print("server")
    print(django.get_version())
    print(DATABASES['default'])