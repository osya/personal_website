from django.conf.urls import url, include
from personal import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^contact/', views.ContactView.as_view(), name='contact'),
]
