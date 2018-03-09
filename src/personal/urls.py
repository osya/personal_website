from django.urls import path

from personal.views import AboutView, ContactView

app_name = 'personal'

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about')
]
