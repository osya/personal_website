from braces.views import FormValidMessageMixin, SetHeadlineMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import ArchiveIndexView, CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.base import ContextMixin, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from blog.forms import PostForm, SearchForm
from blog.models import Post
from blog.serializers import PostSerializer


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


class SearchFormMixin(ContextMixin, View):
    def get_context_data(self, **kwargs):
        context = super(SearchFormMixin, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        return context


class PostList(RestrictToUserMixin, SearchFormMixin, ArchiveIndexView):
    date_field = 'created'
    paginate_by = 10
    allow_empty = True
    allow_future = True
    model = Post

    def get_queryset(self):
        queryset = super(PostList, self).get_queryset()
        return queryset.list(self.request.GET)


class PostListApi(ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.list(self.request.GET)


class PostDetail(RestrictToUserMixin, SearchFormMixin, DetailView):
    model = Post


class PostDetailApi(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.list(self.request.GET)

# TODO: Write tests for the API calls


class PostCreate(
        LoginRequiredMixin,
        SetHeadlineMixin,
        SearchFormMixin,
        FormValidMessageMixin,
        CreateView):
    model = Post
    form_class = PostForm
    headline = 'Add Post'
    form_valid_message = 'Post created'
    # `object = None` is here to avoid PyCharm warnings "Instance attribute object defined outside __init__"
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
        LoginRequiredMixin,
        SetHeadlineMixin,
        SearchFormMixin,
        FormValidMessageMixin,
        RestrictToUserMixin,
        UpdateView):
    model = Post
    form_class = PostForm
    headline = 'Update Post'
    form_valid_message = 'Post updated'

    def get_initial(self):
        initial = super(PostUpdate, self).get_initial()
        initial['publish'] = self.object.published is not None
        return initial


class PostDelete(
        LoginRequiredMixin,
        SearchFormMixin,
        FormValidMessageMixin,
        RestrictToUserMixin,
        DeleteView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        url = reverse('blog:list')
        query = self.request.GET.urlencode()
        if query:
            url = f'{url}?{query}'
        return url

    def get_form_valid_message(self):
        return f'{"Post" if self.object.published is not None else "Draft"} deleted'
