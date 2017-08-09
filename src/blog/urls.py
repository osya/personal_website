from django.conf.urls import url
from .views import BlogView, PostView, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    url(r'^$', BlogView.as_view(), name='list'),
    url(r'^create$', PostCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)$', PostView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update$', PostUpdate.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete$', PostDelete.as_view(), name='delete'),
]
