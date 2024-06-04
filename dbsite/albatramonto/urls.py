from django.urls import path
from . import views

app_name = 'albatramonto'
urlpatterns = [
    path('', views.albatramonto_home, name='home')
]
