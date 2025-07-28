from django.urls import path
from . import views

urlpatterns = [
    path('ceo/', views.ceo_dashboard, name='ceo_dashboard'),
    path('officer/', views.officer_dashboard, name='officer_dashboard'),
]
