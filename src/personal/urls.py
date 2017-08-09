from django.conf.urls import url

from personal import views

urlpatterns = [
    url(r'^contact/', views.ContactView.as_view(), name='contact'),
]
