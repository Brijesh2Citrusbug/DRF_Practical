from django.urls import path

from api.views import *

urlpatterns = [
    path('event/', EventList.as_view(), name='event'),
    path('event/<int:pk>/', EventList.as_view(), name='update_event'),
    path('slot-book/', SlotBookView.as_view(), name='slot_book'),
    path('slot-available/', AvailableSlotList.as_view(), name='slot_book'),
    path('register-user/', RegisterView.as_view(), name='register_user'),
    path('login/', UserLogin.as_view(), name='login'),
]