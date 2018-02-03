"""django_tutorials URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

from post.urls import router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^posts/', include('post.urls', namespace='post')),
    url(r'^api/', include(router.urls)),
    url(r'^personal/', include('personal.urls', namespace='personal')),
    url(r'^comments/', include('django_comments_xtd.urls')),
    url(r'^$', RedirectView.as_view(pattern_name='post:list'), name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^taggit/', include('taggit_selectize.urls')),
    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# TODO: Implement Profile and uploading photo in profile according to the https://github.com/osya/music_website, update
# ImageField & File Uploading Cover letter; add "ImageField" tag to the GitHub
