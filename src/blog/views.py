from django.views.generic import ListView, DetailView
from blog.models import Post


class BlogView(ListView):
    queryset = Post.objects.all().order_by('-date')[:25]
    template_name = 'blog/post_list.jinja'


class PostView(DetailView):
    model = Post
    template_name = 'blog/post_detail.jinja'
