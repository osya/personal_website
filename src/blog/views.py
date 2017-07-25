from django.views.generic import ListView, DetailView
from blog.models import Post
from blog.forms import PostForm


class BlogView(ListView):
    queryset = Post.objects.all().order_by('-date')[:25]


class PostView(DetailView):
    form_class = PostForm
    model = Post

    def get_object(self):
        post = super(PostView, self).get_object()
        return PostForm(instance=post)
