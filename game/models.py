from django.db import models
from user.models import MyUser


class Game(models.Model):
    board = models.TextField()
    status = models.CharField(
        max_length=16,
        choices=[
            ("active", "сейчас играют"),
            ("finished", "законченная"),
            ("waiting", "ожидается"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    winner = models.ForeignKey(
        MyUser,
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="won_games",
    )


class Move(models.Model):
    pass


class GameUser(models.Model):
    pass
