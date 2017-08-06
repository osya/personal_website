from django.views.generic import ListView, DetailView

from blog.models import Post


class BlogView(ListView):
    queryset = Post.objects.all().order_by('-pubdate')
    paginate_by = 10


class PostView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['page'] = self.request.GET.get('page', 1)
        return context
