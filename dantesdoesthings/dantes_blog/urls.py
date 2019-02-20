from django.urls import path

from . import views

urlpatterns = [
    path('', views.dantes_blog, name='dantes_blog'),
    path('/blog/<str:slug>/', views.blog_post, name='blog_post'),
    path('/blog/tags/<str:slug>/', views.blog_tag, name='blog_tag')
]
