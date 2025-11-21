from django.urls import path
from user.views import logout_view
app_name = 'user'

urlpatterns = [
    path('logout', logout_view, name='logout')
]
