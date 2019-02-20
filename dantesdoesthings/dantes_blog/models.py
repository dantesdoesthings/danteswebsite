from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class BlogPost(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateField(db_index=True, auto_now_add=True)
    tags = models.ForeignKey('dantes_blog.Tag', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def url(self):
        return reverse('blog_post', args=[self.slug])


class Tag(models.Model):
    slug = models.SlugField(max_length=100, db_index=True)

    def __str__(self):
        return self.slug

    def url(self):
        return reverse('blog_tag', args=[self.slug])
