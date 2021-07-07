"""dantesdoesthings URL Configuration"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('dantes_site.urls')),
    path('admin/', admin.site.urls),
    path('index/', include('dantes_site.urls')),
    path('data_generator/', include('dantes_data_generator.urls')),
    path('blog/', include('dantes_blog.urls')),
]
