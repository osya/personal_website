from django.conf.urls import url

from personal.views import ContactView

urlpatterns = [
    url(r'^contact/', ContactView.as_view(), name='contact'),
]
