from django.views.generic import ListView, DetailView

from blog.forms import PostForm
from blog.models import Post


class BlogView(ListView):
    queryset = Post.objects.all().order_by('-date')[:25]
    paginate_by = 10


class PostView(DetailView):
    form_class = PostForm
    model = Post

    def get_object(self):
        post = super(PostView, self).get_object()
        return PostForm(instance=post)

    def get_context_data(self, **kwargs):
        page = self.request.GET.get('page', 1)
        context = super(PostView, self).get_context_data(**kwargs)
        context['page'] = page
        return context
