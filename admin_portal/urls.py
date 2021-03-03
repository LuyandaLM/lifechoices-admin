from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views


app_name = 'admin_portal'


urlpatterns = [
    path('', login_required(views.HomePageView.as_view()), name='home'),
    path('covid-questionnaire/', views.CovidQuestionnairePage.as_view(),
         name='covid-questionnaire'),
    path('leave-application/', views.LeaveApplicationPage.as_view(),
         name='leave-application'),
    path('pending-leave-applications/',
         views.PendingLeaveApplicationPage.as_view(), name='pending-leaves'),
    path('chat/', views.ChatPageView.as_view(), name='chat'),
    #path('checkin/', views.CheckinPageView.as_view(), name='check_in'),
    #path('checkinoffsite/', CheckinOffsitePageView.as_view(), name='checkinffsite'),
    path('accountprofile/', views.AccountProfilePageView.as_view(),
         name='accountprofile'),
    path('printusers/', views.PrintUsersPageView.as_view(), name='printusers'),
    path('printcovid/', views.PrintCovidPageView.as_view(), name='printcovid'),
    path('covidfor/', views.CovidForPageView.as_view(), name='covidfor'),
    path('calendar/', views.CalendarPageView.as_view(), name='calendar'),
    path('checkoutlc/', views.CheckOutlcPageView.as_view(), name='checkoutlc'),
    path('checkoutoff/', views.CheckOutoffPageView.as_view(), name='checkoutoff'),
]
