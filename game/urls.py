from django.urls import path, include
from game.views import get_board, create_game, get_moves

urlpatterns = [
    path('get_board', get_board),
    path('create_game', create_game),
    path('get_moves', get_moves)
]

