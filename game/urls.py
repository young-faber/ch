from django.urls import path
from game.views import get_board, create_game, get_moves, move_figure

urlpatterns = [
    path('get_board/<int:pk>', get_board, name='get_board'),
    path('create_game/', create_game, name='create_game'),
    path('get_moves/<int:pk>/', get_moves, name='get_moves'),
    path('move_figure/<int:pk>/', move_figure, name='move_figure')
]