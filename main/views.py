from django.shortcuts import redirect
from user.forms import LoginForm
from django.contrib import auth
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView

# load_dotenv()

class IndexView(LoginView):
    form_class = LoginForm
    authentication_form = LoginForm
    template_name = "main/index.html"
    redirect_authenticated_user = True

    

def lobby(request): 
    return redirect('/')