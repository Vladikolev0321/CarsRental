from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='carsRental-Home'),
    path('about/', views.about, name='carsRental-about'),
]