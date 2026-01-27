from django.urls import path
from user.views import  RegistrView
from main.views import IndexView, lobby
app_name = 'main'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("lobby", lobby, name="lobby"),
    path('registr', RegistrView.as_view(), name='registr')
]
