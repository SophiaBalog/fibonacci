from . import views
from django.urls import path

urlpatterns = [
    path('fibonacci/<int:n>/', views.fibonacci, name='fibonacci'),
]

