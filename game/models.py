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
        default="waiting"
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
    white = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        related_name='game_as_white'
    )
    black = models.ForeignKey(
            MyUser, 
            on_delete=models.CASCADE,
            default=None,
            null=True,
            blank=True,
            related_name='game_as_black'
        )
    
    current = models.CharField(
        max_length=10, choices=[("white", "white"), ("black", "black")], default="white"
    )


class GameUser(models.Model):
    """$"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class Move(models.Model):
    pass
