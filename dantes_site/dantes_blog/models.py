from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class BlogPost(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=32, unique=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextUploadingField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
