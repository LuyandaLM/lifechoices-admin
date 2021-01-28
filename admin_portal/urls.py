from django.urls import path, include
from .views import HomePageView

app_name = 'admin_portal'


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('api/', include('admin_portal.api.urls'))
]
