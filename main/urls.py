from django.urls import path
from main.views import IndexView, lobby, RegistrView
app_name = 'main'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("lobby", lobby, name="lobby"),
    path('registr', RegistrView.as_view(), name='registr')
]
