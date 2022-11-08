from django.urls import path

from . import views


urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('archive', views.blog_archive, name='blog_archive'),
    path('post/<str:slug>/', views.blog_post, name='blog_post'),
]
