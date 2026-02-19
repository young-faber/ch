from django.shortcuts import redirect
from django.contrib import auth
from user.forms import RegistrForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login
import random
from django.core.mail import EmailMultiAlternatives, send_mail


def logout_view(request):
    auth.logout(request)
    return redirect("/")


class RegistrView(FormView):
    form_class = RegistrForm
    template_name = "main/registr.html"
    success_url = reverse_lazy("main:verification")

    def form_valid(self, form):
        user = form.save(commit=False)
        code = "".join([str(random.randint(0, 9)) for i in range(6)])
        user.code = code
        user.save()
        send_mail(subject="код для верификации в шахматах",
            message=f"Вы пытаетесь зарегестрироваться в онлайн шахматах, введите следующий код в браузерном окне {code}",
            from_email="MarsEisen@yandex.com",
            recipient_list=[user.email],
            fail_silently=False)
        print('email was sent')
       
        login(self.request, user)
        # здесь мы должны сделать
        return super().form_valid(form)
