from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Register, profile, PendingAccounts, ActivatePendingAccount, activate_account, ViewProfile

app_name = 'users'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('register/', Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('pending-accounts/', PendingAccounts.as_view(), name='pending-accounts'),
    path('pending-accounts/<int:pk>', ActivatePendingAccount.as_view(),
         name='activate-pending-accounts'),
    path('activate-account/<int:pk>', activate_account, name='activate-account'),
    path('view-profile/', ViewProfile.as_view(), name='viewprofile'),

]
