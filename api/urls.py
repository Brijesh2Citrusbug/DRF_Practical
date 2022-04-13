from django.urls import path

from api.views import EventView

urlpatterns = [
    path('event-create/', EventView.as_view()),
]