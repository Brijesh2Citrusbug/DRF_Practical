from django.urls import path

from api.views import *

urlpatterns = [
    path('event/', EventList.as_view(), name='event'),
    path('event/<int:pk>/', EventView.as_view(), name='update_event'),
    path('register-user/', RegisterView.as_view(), name='register_user'),
    path('login/', UserLogin.as_view(), name='login'),
]