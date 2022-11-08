"""dantes_site URL Configuration"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('', include('site_base.urls')),
    path('admin/', admin.site.urls),
    path('data_generator/', include('dantes_data_generator.urls')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('blog/', include(('dantes_blog.urls', 'blog'), namespace='blog')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.dev_mode:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
