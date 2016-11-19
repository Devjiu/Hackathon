import django
from untitled.settings import DATABASES


def print_hui():
    print("Hui!")

if __name__ == '__main__':
    print("server")
    print(django.get_version())
    print(DATABASES['default'])