from django.urls import path
from . import views

app_name = 'suono'
urlpatterns = [
    path('', views.suono_home, name='home')
]
