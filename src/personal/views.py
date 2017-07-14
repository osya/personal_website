from django.shortcuts import render


def index(request):
    return render(request, 'personal/home.jinja')


def contact(request):
    return render(request, 'personal/basic.jinja', {'content': ['If you would like to contact me, please email me',
                                                               'info@vosipov.com']})
