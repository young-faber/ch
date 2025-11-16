from django.urls import path
from main.views import (
    IndexView,
    lobby
)


urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path("lobby/", lobby, name='lobby')
    ]
