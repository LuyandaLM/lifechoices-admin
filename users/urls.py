from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Register, profile, PendingAccounts, ActivatePendingAccount, activate_account, ViewProfile, \
    AdminPageView, RegistrationConfirmation, update_profile, update_bankingdetails, update_kin_details, update_contact_details


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
    path('activate-account/<int:pk>', activate_account, name='activate-account'),
    path('view-profile/', ViewProfile.as_view(), name='view-profile'),
    path('admin-page/', AdminPageView.as_view(), name='admin'),
    # path('account-profile/', AccountProfilePageView.as_view(), name='accountprofile'),
    path('registration-confirmation/', RegistrationConfirmation.as_view(), name='registration-confirmation'),
    path('update-profile/<int:pk>/', update_profile, name='updateprofile'),
    path('update-banking-details/', update_bankingdetails, name='updatebankingdetails'),
    path('update-kin-details/', update_kin_details, name='updatekin'),
    path('update-contact-details/', update_contact_details, name='updatecontact')
]
