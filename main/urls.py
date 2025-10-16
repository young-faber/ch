from django.urls import path
from main.views import (
    IndexView,
    lobby
)


urlpatterns = [
    path("", IndexView.as_view()),
    path("lobby/", lobby, name='lobby')
    ]
