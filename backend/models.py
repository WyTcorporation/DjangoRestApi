from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=250, unique=True)
    published = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='article')

    def __str__(self):
        return self.title
