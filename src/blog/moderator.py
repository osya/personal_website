#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django_comments_xtd.moderation import XtdCommentModerator, moderator

from blog.models import Post


class BlogModerator(XtdCommentModerator):
    email_notification = True
    enable_field = 'is_commentable'


moderator.register(Post, BlogModerator)
