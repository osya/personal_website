from django.contrib import admin
from .models import Post
from django_markdown.admin import MarkdownModelAdmin


class PostAdmin(MarkdownModelAdmin):
    list_display = ('title', 'created')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
