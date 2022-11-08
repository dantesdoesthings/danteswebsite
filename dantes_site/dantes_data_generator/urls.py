from django.urls import path

from . import views


urlpatterns = [
    path('', views.data_generator, name='data_generator'),
    path('submit_data', views.submit_data, name='submit_generator_data'),
]
