from django.shortcuts import render, redirect
from user.forms import LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import MyUser
from game.models import Game
from django.db.models import Q  

class IndexView(LoginView):
    form_class = LoginForm
    authentication_form = LoginForm
    template_name = "main/index.html"
    redirect_authenticated_user = True

    

@login_required
def lobby(request): 
    if request.user and not request.user.is_verified:
        #return redirect('main:lobby')
        pass
    
    # Подсчитать количество завершённых игр пользователя
    games_played = Game.objects.filter(
        Q(white=request.user) | Q(black=request.user),  # Белые ИЛИ Чёрные фигуры
        status="finished"  # И статус "завершена"
    ).count()
    
    return render(request, 'main/lobby.html', {'games_played': games_played})


def verification(request):
    if request.method == 'GET':
        return render(request, 'main/verification.html')
    else:
        code = request.POST.get('code')
        if code == request.user.code:
            request.user.is_verified = True
            request.user.save()
            return redirect('main:lobby')
        else:
            messages.error(request, 'неверный код')
            return render(request, 'main/verification.html')