from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import HomePageView, CovidQuestionnairePage


app_name = 'admin_portal'


urlpatterns = [
    path('', login_required(HomePageView.as_view()), name='home'),
    path('/covid-questionnaire', CovidQuestionnairePage.as_view(), name='covid-questionnaire'),
    path('api/', include('admin_portal.api.urls'))
]
