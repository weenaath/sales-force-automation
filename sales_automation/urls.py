from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='sales_automation/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]