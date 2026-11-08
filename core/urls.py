from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_faculty_view, name='register'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('redirect/', views.dashboard_redirect_view, name='dashboard_redirect'),
]

