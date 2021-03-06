# noinspection PyPackageRequirements
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse

from autoslug import AutoSlugField
from django_markdown.models import MarkdownField
from taggit_selectize.managers import TaggableManager


class PostQuerySet(models.QuerySet):
    def list(self, query_dict=None):
        if query_dict is None:
            query_dict = {}
        queryset = self.filter(published__isnull='draft' in query_dict)
        tags = query_dict.get('tags')
        if tags:
            tags = tags.split(',')
            queryset = queryset.filter(tags__name__in=tags).distinct()
        query = query_dict.get('query')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(body__icontains=query)).distinct()
        return queryset


class Post(models.Model):
    # pragma pylint: disable=R0903
    class Meta:
        ordering = ('-created', )
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    # pragma pylint: enable=R0903

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=100, unique_for_date='created')
    body = MarkdownField()
    slug = AutoSlugField(populate_from='title', unique=True)
    is_commentable = models.BooleanField(default=True)
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    published = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug': self.slug})
