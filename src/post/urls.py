from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from post.views import PostCreate, PostDelete, PostDetail, PostDetailApi, PostList, PostListApi, PostUpdate

post_api_patterns = [
    url(r'^$', PostListApi.as_view()),
    url(r'^(?P<pk>\d+)/$', PostDetailApi.as_view())
]

urlpatterns = [
    url(r'^$', PostList.as_view(), name='list'),
    url(r'^create/$', PostCreate.as_view(), name='create'),
    url(r'^(?P<slug>[-\w]+)/$', PostDetail.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w]+)/update/$', PostUpdate.as_view(), name='update'),
    url(r'^(?P<slug>[-\w]+)/delete/$', PostDelete.as_view(), name='delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# TODO: Add RSS/Atom
