from django.shortcuts import redirect
from user.forms import LoginForm
from django.contrib import auth
from django.views.generic.base import TemplateView

# load_dotenv()

class IndexView(TemplateView):
    template_name = "game/index.html"

    def get(self, request, *args, **kwargs):
        login_form = LoginForm()
        context = {"login_form": login_form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(data=request.POST)

        if login_form.is_valid():
            username = request.POST.get("username")

            password = request.POST.get("password")

            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect("/")

        context = {"login_form": login_form}
        return self.render_to_response(context)

def lobby(): 
    pass