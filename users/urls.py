from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Register, profile

app_name = 'users'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('register/', Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
]

