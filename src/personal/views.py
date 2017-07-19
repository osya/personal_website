from django.shortcuts import render_to_response


def index(request):
    return render_to_response('personal/home.jinja')


def contact(request):
    context = {'content': ['If you would like to contact me, please email me', 'info@vosipov.com']}
    return render_to_response('personal/basic.jinja', context)
