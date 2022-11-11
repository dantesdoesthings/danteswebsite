from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class BlogTag(models.Model):
    tag = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=100, default='')

    class Meta:
        ordering = ['tag']

    def __str__(self):
        return self.tag


class BlogPost(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=32, unique=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextUploadingField()
    created_on = models.DateTimeField(auto_now_add=True)
    blog_tags = models.ManyToManyField(BlogTag)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
