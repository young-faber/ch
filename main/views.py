from django.shortcuts import render
from user.forms import LoginForm
from django.contrib.auth.views import LoginView

# load_dotenv()

class IndexView(LoginView):
    form_class = LoginForm
    authentication_form = LoginForm
    template_name = "main/index.html"
    redirect_authenticated_user = True

    


def lobby(request): 
    return render(request, 'main/lobby.html')
