from django.contrib import admin
from .models import BlogTag, BlogPost

admin.site.register(BlogPost)
admin.site.register(BlogTag)
