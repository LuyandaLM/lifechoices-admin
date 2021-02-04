from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import HomePageView


app_name = 'admin_portal'


urlpatterns = [
    path('', login_required(HomePageView.as_view()), name='home'),
    path('api/', include('admin_portal.api.urls'))
]
