from braces import views
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ArchiveIndexView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from .forms import PostForm
from .models import Post


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


class BlogView(RestrictToUserMixin, ArchiveIndexView):
    model = Post
    date_field = 'posted'
    paginate_by = 10
    allow_empty = True
    allow_future = True

    def get_queryset(self):
        # TODO: Move to Model Manager
        queryset = super(BlogView, self).get_queryset()
        tags = self.request.GET.get('tags')
        if tags:
            tags = tags.split(',')
            queryset = queryset.filter(tags__name__in=tags).distinct()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                    Q(title__icontains=q) |
                    Q(description__icontains=q) |
                    Q(content__icontains=q)).distinct()
        return queryset


class PostView(RestrictToUserMixin, DetailView):
    model = Post


class PostCreate(
        views.SetHeadlineMixin,
        LoginRequiredMixin,
        views.FormValidMessageMixin,
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
        views.SetHeadlineMixin,
        LoginRequiredMixin,
        views.FormValidMessageMixin,
        SuccessUrlMixin,
        RestrictToUserMixin,
        UpdateView):
    model = Post
    form_class = PostForm
    headline = 'Update Post'
    form_valid_message = 'Post updated'


class PostDelete(
        LoginRequiredMixin,
        views.FormValidMessageMixin,
        SuccessUrlMixin,
        RestrictToUserMixin,
        DeleteView):
    model = Post
    form_class = PostForm
    form_valid_message = 'Post deleted'
