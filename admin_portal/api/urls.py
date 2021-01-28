from django.urls import path
from .views import CovidList, LeaveList, MyObtainTokenPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('covid-questionnaire/', CovidList.as_view()),
    path('leave/', LeaveList.as_view(), name='leave_application'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]
