from django.core.urlresolvers import reverse
from django.db import models
from precise_bbcode.fields import BBCodeTextField


class Post(models.Model):
    title = models.CharField(max_length=140, unique_for_date='pubdate')
    body = BBCodeTextField()
    pubdate = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'pk': self.pk})
