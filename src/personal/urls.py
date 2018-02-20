from django.urls import path

from personal.views import ContactView

app_name = 'personal'

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
]
