from django.db import models
from datetime import datetime


class Post(models.Model):
    title = models.CharField(max_length=140)
    body = models.TextField()
    date = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.title
