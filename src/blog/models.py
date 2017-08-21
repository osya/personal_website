from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from precise_bbcode.fields import BBCodeTextField
from taggit_selectize.managers import TaggableManager


class Post(models.Model):
    class Meta:
        ordering = ('-posted',)
        verbose_name = 'blog post'
        verbose_name_plural = 'blog posts'

    title = models.CharField(max_length=100, unique_for_date='posted')
    description = models.TextField(null=True, blank=True)
    body = BBCodeTextField()
    is_commentable = models.BooleanField(default=True)
    tags = TaggableManager(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    posted = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
