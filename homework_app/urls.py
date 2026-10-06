from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculate_view, name='calculate_home'),
    path('calculate/', views.calculate_view, name='calculate'),
    path('result/', views.result_view, name='result'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('rating/', views.rating_view, name='rating'),
]