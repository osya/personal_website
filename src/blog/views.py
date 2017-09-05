from braces.views import FormValidMessageMixin, SetHeadlineMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import ArchiveIndexView, CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from blog.forms import PostForm
from blog.models import Post
from blog.serializers import PostSerializer


class SuccessUrlMixin(View):
    def get_success_url(self):
        url = reverse('blog:list')
        query = self.request.GET.urlencode()
        if query:
            url = f'{url}?{query}'
        return url


class RestrictToUserMixin(View):
    object = None

    def get_queryset(self):
        assert isinstance(self, (SingleObjectMixin, MultipleObjectMixin))
        assert isinstance(self, View)
        queryset = super(RestrictToUserMixin, self).get_queryset()
        if self.request.user.is_authenticated() and not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        assert isinstance(self, SingleObjectMixin)
        self.object = self.get_object()
        assert isinstance(self, View)
        return super(RestrictToUserMixin, self).post(request, *args, **kwargs) \
            if self.request.user == self.object.user or self.request.user.is_superuser \
            else redirect(reverse('login'))


class PostList(RestrictToUserMixin, ArchiveIndexView):
    date_field = 'created'
    paginate_by = 10
    allow_empty = True
    allow_future = True

    def get_queryset(self):
        return Post.objects.list(self.request.GET)


class PostListApi(ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.list(self.request.GET)


class PostDetail(RestrictToUserMixin, DetailView):
    model = Post


class PostDetailApi(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.list(self.request.GET)

# TODO: Write tests for the API calls


class PostCreate(
        SetHeadlineMixin,
        LoginRequiredMixin,
        FormValidMessageMixin,
        SuccessUrlMixin,
        CreateView):
    model = Post
    form_class = PostForm
    headline = 'Add Post'
    form_valid_message = 'Post created'
    object = None

    def get_initial(self):
        initial = super(PostCreate, self).get_initial()
        if self.request.GET.get('tags'):
            initial['tags'] = self.request.GET.get('tags')
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(PostCreate, self).form_valid(form)


class PostUpdate(
        SetHeadlineMixin,
        LoginRequiredMixin,
        FormValidMessageMixin,
        SuccessUrlMixin,
        RestrictToUserMixin,
        UpdateView):
    model = Post
    form_class = PostForm
    headline = 'Update Post'
    form_valid_message = 'Post updated'


class PostDelete(
        LoginRequiredMixin,
        FormValidMessageMixin,
        SuccessUrlMixin,
        RestrictToUserMixin,
        DeleteView):
    model = Post
    form_class = PostForm
    form_valid_message = 'Post deleted'
