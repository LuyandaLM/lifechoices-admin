from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Register, profile
from admin_portal.api.views import MyObtainTokenPairView

app_name = 'users'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('register/', Register.as_view(), name='register'),
    path('login/', MyObtainTokenPairView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
]

