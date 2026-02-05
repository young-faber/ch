from django.shortcuts import render, redirect
from user.forms import LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
# load_dotenv()

class IndexView(LoginView):
    form_class = LoginForm
    authentication_form = LoginForm
    template_name = "main/index.html"
    redirect_authenticated_user = True

    

@login_required
def lobby(request): 
    if request.user and not request.user.is_verifed:
        #return redirect('main:lobby')
        pass
    return render(request, 'main/lobby.html')
