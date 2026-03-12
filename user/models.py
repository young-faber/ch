from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    img = models.ImageField(upload_to='img_user', default='img_user/default.png')
    code = models.CharField(max_length=6, default='123456')
    is_verified = models.BooleanField(default=False)


    