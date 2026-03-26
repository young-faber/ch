from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from user.models import MyUser

class LoginForm(AuthenticationForm):
    class Meta:     
        model = MyUser
        fields = ['username', 'password']


class RegistrForm(UserCreationForm):
    class Meta: 
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username':'имя пользователя',
            'email':'email',
            'password':'введите пароль',
            'password2':'потвердите пароль'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = 'введите пароль'
        self.fields['password2'].label = 'потвердите пароль'