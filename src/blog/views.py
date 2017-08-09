from braces import views
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ArchiveIndexView
from django.views.generic.base import ContextMixin, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from .forms import PostForm
from .models import Post


class PageContextMixin(ContextMixin, View):
    def get_context_data(self, **kwargs):
        context = super(PageContextMixin, self).get_context_data(**kwargs)
        context['page'] = int(self.request.GET.get('page', 1))
        return context


class SuccessUrlMixin(View):
    def get_success_url(self):
        url = reverse('blog:list')
        page = self.request.GET.get('page')
        if page and int(page) > 1:
            url = f'{url}?page={page}'
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


class PostView(PageContextMixin, RestrictToUserMixin, DetailView):
    model = Post


class PostCreate(
        views.SetHeadlineMixin,
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        PageContextMixin,
        SuccessUrlMixin,
        CreateView):
    model = Post
    form_class = PostForm
    headline = 'Add Post'
    form_valid_message = 'Post created'
    object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(PostCreate, self).form_valid(form)


class PostUpdate(
        views.SetHeadlineMixin,
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        PageContextMixin,
        SuccessUrlMixin,
        RestrictToUserMixin,
        UpdateView):
    model = Post
    form_class = PostForm
    headline = 'Update Post'
    form_valid_message = 'Post updated'


class PostDelete(
        views.LoginRequiredMixin,
        views.FormValidMessageMixin,
        PageContextMixin,
        SuccessUrlMixin,
        RestrictToUserMixin,
        DeleteView):
    model = Post
    form_class = PostForm
    form_valid_message = 'Post deleted'
