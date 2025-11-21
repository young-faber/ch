from django.urls import path
from game.views import get_board, create_game, get_moves, move_figure, render_game, pawn_promotion, join_game
app_name = 'game'

urlpatterns = [
    path('get_board/<int:pk>', get_board, name='get_board'),
    path('create_game/', create_game, name='create_game'),
    path('get_moves/<int:pk>/', get_moves, name='get_moves'),
    path('move_figure/<int:pk>/', move_figure, name='move_figure'),
    path('<int:pk>', render_game, name='render_game'),
    path('pawn_promotion', pawn_promotion, name='pawn_promotion'),
    path('join_game', join_game, name='join_game')
]