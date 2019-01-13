"""dantesdoesthings URL Configuration"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('index.urls')),
    path('index/', include('index.urls')),
    path('admin/', admin.site.urls),
]
