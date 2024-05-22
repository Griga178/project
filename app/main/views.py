from django.shortcuts import render
from django.apps import apps

# Create your views here.

def index(request):
    # HOME PAGE
    # app_list = apps.get_models()
    # for app in app_list:
    #     for i,v in app.__dict__.items():
    #         print(i,v)
    #     print('\n\n')
    # print(apps.__dict__)

    # for i,v in apps.__dict__.items():
    #     print(i,v)
    # print('\n\n')

    return render(request, 'main/main.html')

def feautures_info(request):
    pass
