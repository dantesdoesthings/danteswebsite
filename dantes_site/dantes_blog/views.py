import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpRequest

from .models import BlogPost


def blog_home(request: HttpRequest):
    recent_blogs = BlogPost.objects.order_by('-created_on')[:5]
    context = {
        'recent_blogs': recent_blogs,
    }
    return render(request, 'dantes_blog/blog_home.html', context=context)


def blog_archive(request: HttpRequest):
    return render(request, 'dantes_blog/blog_archive.html')


def blog_post(request: HttpRequest, slug: str):
    bp = get_object_or_404(BlogPost, slug=slug)
    context = {
        'blog': bp,
    }
    return render(request, f'dantes_blog/blog_post.html', context=context)
