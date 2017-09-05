from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from django_markdown.models import MarkdownField
from taggit_selectize.managers import TaggableManager


class PostQuerySet(models.QuerySet):
    def list(self, query_dict={}):
        queryset = self.filter(publish=True)
        tags = query_dict.get('tags')
        if tags:
            tags = tags.split(',')
            queryset = queryset.filter(tags__name__in=tags).distinct()
        q = query_dict.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(content__icontains=q)).distinct()
        return queryset


class Post(models.Model):
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    title = models.CharField(max_length=100, unique_for_date='created')
    description = models.TextField(null=True, blank=True)
    body = MarkdownField()
    slug = models.SlugField(max_length=200, unique=True)
    is_commentable = models.BooleanField(default=True)
    tags = TaggableManager(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)
