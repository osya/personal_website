from django.contrib import admin

from django_markdown.admin import MarkdownModelAdmin

from post.models import Post


class PostAdmin(MarkdownModelAdmin):
    list_display = ('title', 'created')
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Post, PostAdmin)
