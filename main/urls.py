from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('booking/', views.register, name='register'),
    path('register/', views.register_client, name='register_client'),
    path('tour_info/', views.tour_info, name='tour_info'),
    path('success/', views.success_view, name='success_view'),
    path('terms/', views.terms_view, name='terms_view'), 
    path('privacy/', views.privacy_view, name='privacy_view'),
    path('partner/', views.partnership_view, name='partner_view'),
]