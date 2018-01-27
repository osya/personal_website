from braces.views import FormValidMessageMixin, SetHeadlineMixin
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import ArchiveIndexView, CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.base import ContextMixin, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from post.forms import PostForm, SearchForm
from post.models import Post
from post.serializers import CreatePostSerializer, PostSerializer


class RestrictToUserGetMixin(View):
    def get_queryset(self):
        assert isinstance(self, (SingleObjectMixin, MultipleObjectMixin))
        queryset = super(RestrictToUserGetMixin, self).get_queryset()
        if self.request.user.is_authenticated() and not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class RestrictToUserPostMixin(View):
    object = None

    def post(self, request):
        assert isinstance(self, SingleObjectMixin)
        self.object = self.get_object()
        return super(RestrictToUserPostMixin, self).post(request, ) \
            if self.request.user == self.object.user or self.request.user.is_superuser \
            else redirect(reverse('login'))


class SearchFormMixin(ContextMixin, View):
    # It is to disable warnings 'Unresolved attribute reference `request`'
    request = None

    def get_context_data(self, **kwargs):
        context = super(SearchFormMixin, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        return context


class PostList(AccessMixin, RestrictToUserGetMixin, SearchFormMixin, ArchiveIndexView):
    date_field = 'created'
    paginate_by = 10
    allow_empty = True
    allow_future = True
    model = Post

    def get_queryset(self):
        queryset = super(PostList, self).get_queryset()
        return queryset.list(self.request.GET)

    # Require login if `draft` query parameter exists. It is modified method from LoginRequiredMixin
    def dispatch(self, request, *args, **kwargs):
        return self.handle_no_permission() if 'draft' in request.GET and not request.user.is_authenticated \
            else super(PostList, self).dispatch(request, *args, **kwargs)


class PostListApi(AccessMixin, RestrictToUserGetMixin, ListCreateAPIView):
    def get_serializer_class(self):
        return CreatePostSerializer if 'POST' == self.request.method else PostSerializer

    def get_queryset(self):
        return Post.objects.list(self.request.GET)

    # Require login if `draft` query parameter exists. It is modified method from LoginRequiredMixin
    def dispatch(self, request, *args, **kwargs):
        return self.handle_no_permission() if 'draft' in request.GET and not request.user.is_authenticated \
            else super(PostListApi, self).dispatch(request, *args, **kwargs)


class PostDetail(RestrictToUserGetMixin, SearchFormMixin, DetailView):
    model = Post


class PostDetailApi(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.list(self.request.GET)
        if self.request.user.is_authenticated() and not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        return super(PostDetailApi, self).patch(request, *args, **kwargs) \
            if self.request.user == instance.user or self.request.user.is_superuser \
            else redirect(reverse('login'))

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        return super(PostDetailApi, self).patch(request, *args, **kwargs) \
            if self.request.user == instance.user or self.request.user.is_superuser \
            else redirect(reverse('login'))

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        return super(PostDetailApi, self).delete(self) \
            if self.request.user == instance.user or self.request.user.is_superuser \
            else redirect(reverse('login'))

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
        RestrictToUserPostMixin,
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
        RestrictToUserPostMixin,
        DeleteView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        url = reverse('post:list')
        query = self.request.GET.urlencode()
        if query:
            url = f'{url}?{query}'
        return url

    def get_form_valid_message(self):
        return f'{"Post" if self.object.published is not None else "Draft"} deleted'
