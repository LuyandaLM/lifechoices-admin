from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Register, RegisterParttwo, PendingAccounts, ActivatePendingAccount, activate_account, ViewProfile, AdminPageView, \
    RegistrationConfirmation, update_profile, update_bankingdetails, update_kin_details, update_contact_details


app_name = 'users'

urlpatterns = [
    #path('profile/', views.profile, name='profile'),
    path('register/', Register.as_view(), name='register'),
    path('register/part2/', RegisterParttwo.as_view(), name='registerp2'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('pending-accounts/', PendingAccounts.as_view(), name='pending-accounts'),
    path('pending-accounts/<int:pk>', ActivatePendingAccount.as_view(),
         name='activate-pending-accounts'),
    path('activate-account/<int:pk>', activate_account, name='activate-account'),
    path('view-profile/', ViewProfile.as_view(), name='view-profile'),
    path('admin-page/', AdminPageView.as_view(), name='admin'),
    # path('account-profile/', AccountProfilePageView.as_view(), name='accountprofile'),
    path('registration-confirmation/', RegistrationConfirmation.as_view(),
         name='registration-confirmation'),
    path('update-profile/<int:pk>/', update_profile, name='update-profile'),
    path('update-banking-details/', update_bankingdetails,
         name='update-banking-details'),
    path('update-kin-details/', update_kin_details, name='update-kin'),
    path('update-contact-details/', update_contact_details, name='update-contact')
]
