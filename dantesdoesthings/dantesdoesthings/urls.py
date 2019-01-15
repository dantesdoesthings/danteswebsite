"""dantesdoesthings URL Configuration"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('dantes_site.urls')),
    path('index/', include('dantes_site.urls')),
    path('data_generator/', include('dantes_data_generator.urls')),
    path('admin/', admin.site.urls),
]
