from django.urls import path
from . import views

urlpatterns = [
    path('', views.affiliate_program, name='affiliate_program'),
    path('register/', views.affiliate_register, name='affiliate_register'),
    path('complete/', views.register_complete, name='complete'),
    path('success/', views.affiliate_success, name='affiliate_success'),
]
