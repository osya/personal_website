from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from post.views import PostCreate, PostDelete, PostDetail, PostList, PostUpdate, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, base_name='post')

urlpatterns = [
    url(r'^$', PostList.as_view(), name='list'),
    url(r'^create/$', PostCreate.as_view(), name='create'),
    url(r'^(?P<slug>[-\w]+)/$', PostDetail.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w]+)/update/$', PostUpdate.as_view(), name='update'),
    url(r'^(?P<slug>[-\w]+)/delete/$', PostDelete.as_view(), name='delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# TODO: Add RSS/Atom
