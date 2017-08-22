from django.conf.urls import url

from blog.views import BlogView, PostCreate, PostView, PostUpdate, PostDelete

urlpatterns = [
    url(r'^$', BlogView.as_view(), name='list'),
    url(r'^create$', PostCreate.as_view(), name='create'),
    url(r'^(?P<slug>[-\w]+)$', PostView.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w]+)/update$', PostUpdate.as_view(), name='update'),
    url(r'^(?P<slug>[-\w]+)/delete$', PostDelete.as_view(), name='delete'),
]

# TODO: Add RSS/Atom
