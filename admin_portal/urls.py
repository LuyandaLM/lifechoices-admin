from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import HomePageView, CovidQuestionnairePage, LeaveApplicationPage, PendingLeaveApplicationPage, ChatPageView,\
    AdminPageView


app_name = 'admin_portal'


urlpatterns = [
    path('', login_required(HomePageView.as_view()), name='home'),
    path('covid-questionnaire/', CovidQuestionnairePage.as_view(), name='covid-questionnaire'),
    path('leave-application/', LeaveApplicationPage.as_view(), name='leave-application'),
    path('pending-leave-applications/', PendingLeaveApplicationPage.as_view(), name='pending-leaves'),
    path('api/', include('admin_portal.api.urls')),
    path('chat/', ChatPageView.as_view(), name='chat'),
    path('adminpage/', AdminPageView.as_view(), name='admin'),
]
