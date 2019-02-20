from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import BlogPost, Tag


def dantes_blog(request):
    posts = BlogPost.objects.filter(posted__lte=timezone.now()).order_by('posted')
    tags = Tag.objects.all()
    return render(request, 'dantes_blog/blog.html', {'posts': posts, 'tags': tags})


def blog_post(request, slug):
    return render(request, 'dantes_blog/blog_post.html', {'post': get_object_or_404(BlogPost, slug=slug)})


def blog_tag(request, slug):
    return render(request, 'dantes_blog/view_tag.html',
                  {'tag': slug, 'posts': BlogPost.objects.filter(tags__slug__contains=slug)})
