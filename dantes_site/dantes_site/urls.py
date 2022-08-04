"""dantes_site URL Configuration"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('site_base.urls')),
    path('admin/', admin.site.urls),
    path('data_generator/', include('dantes_data_generator.urls')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
]
