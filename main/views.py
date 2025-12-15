from django.shortcuts import render, redirect
from user.forms import LoginForm, RegistrForm
from django.contrib import auth
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login

# load_dotenv()

class IndexView(LoginView):
    form_class = LoginForm
    authentication_form = LoginForm
    template_name = "main/index.html"
    redirect_authenticated_user = True

class RegistrView(FormView):
    form_class = RegistrForm
    template_name = 'main/registr.html'
    success_url = reverse_lazy('main:lobby')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    


def lobby(request): 
    return render(request, 'main/lobby.html')
