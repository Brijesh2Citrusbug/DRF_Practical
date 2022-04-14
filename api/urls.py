from django.urls import path

from api.views import *

urlpatterns = [
    path('event-create/', EventView.as_view()),
    path('register-user/', RegisterView.as_view()),
    path('login/', UserLogin.as_view()),
]