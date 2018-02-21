from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from personal_website.urls import ROUTER
from post.views import PostCreate, PostDelete, PostDetail, PostList, PostUpdate, PostViewSet

app_name = 'post'

ROUTER.register('posts', PostViewSet, base_name='post')

urlpatterns = [
    path('', PostList.as_view(), name='list'),
    path('create/', PostCreate.as_view(), name='create'),
    path('<slug:slug>/', PostDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', PostUpdate.as_view(), name='update'),
    path('<slug:slug>/delete/', PostDelete.as_view(), name='delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# TODO: Add RSS/Atom
