from django.shortcuts import render, redirect
from user.forms import LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

def verification(request):
    if request.method == 'GET':
        return render(request, 'main/verification.html')
    else:
        code = request.POST.get('code')
        if code == request.user.code:
            request.user.is_verifed = True
            request.user.save()
            return redirect('main:lobby')
        else:
            messages.error(request, 'неверный код')
            return render(request, 'main/verification.html')