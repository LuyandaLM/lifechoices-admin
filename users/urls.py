from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    #path('profile/', views.profile, name='profile'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('pending-accounts/', views.PendingAccounts.as_view(),
         name='pending-accounts'),
    path('pending-accounts/<int:pk>', views.ActivatePendingAccount.as_view(),
         name='activate-pending-accounts'),
    path('activate-account/<int:pk>',
         views.activate_account, name='activate-account'),
    path('view-profile/', views.ViewProfile.as_view(), name='viewprofile'),
    path('update-profile/<int:pk>/',
         views.update_profile, name='updateprofile'),
    path('update-banking-details/',
         views.update_bankingdetails, name='updatebankingdetails'),
    path('update-kin-details/', views.update_kin_details, name='updatekin'),
    path('update-contact-details/',
         views.update_contact_details, name='updatecontact')

]
