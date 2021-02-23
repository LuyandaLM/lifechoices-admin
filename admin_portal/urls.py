from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import HomePageView, CovidQuestionnairePage, LeaveApplicationPage, PendingLeaveApplicationPage, ChatPageView,\
    CheckinPageView, AdminPageView, CheckinPageView, AccountProfilePageView, PrintUsersPageView, PrintCovidPageView, CheckinOffsitePageView


app_name = 'admin_portal'


urlpatterns = [
    path('', login_required(HomePageView.as_view()), name='home'),
    path('covid-questionnaire/', CovidQuestionnairePage.as_view(), name='covid-questionnaire'),
    path('leave-application/', LeaveApplicationPage.as_view(), name='leave-application'),
    path('pending-leave-applications/', PendingLeaveApplicationPage.as_view(), name='pending-leaves'),
    path('api/', include('admin_portal.api.urls')),
    path('chat/', ChatPageView.as_view(), name='chat'),
    path('checkin/', CheckinPageView.as_view(), name='checkin'),
    path('checkinoffsite/', CheckinOffsitePageView.as_view(), name='checkinffsite'),
    path('accountprofile/', AccountProfilePageView.as_view(), name='accountprofile'),
    path('printusers/', PrintUsersPageView.as_view(), name='printusers'),
    path('printcovid/', PrintCovidPageView.as_view(), name='printcovid'),
]
