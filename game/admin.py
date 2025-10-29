from django.contrib import admin
from game.models import Game, GameUser

# Register your models here.
admin.site.register([Game, GameUser])