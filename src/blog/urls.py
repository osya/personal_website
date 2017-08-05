from django.conf.urls import url
from .views import BlogView, PostView

urlpatterns = [
    url(r'^(?P<pk>\d+)$', PostView.as_view()),
    url(r'^(?:page/(?P<page>\d+))?$', BlogView.as_view(), name='blog'),
]
