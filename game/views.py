from django.shortcuts import render
from django.http.response import JsonResponse
from game.chess_board import Game
from game.chess_pieces import *
# from .models import Game  # если у тебя есть модель Game

game = Game()
game.calc_attack_map('white')
game.calc_attack_map('black')

# Create your views here.
def create_game(request):
    # request.session['game'] = game
    return render(request, 'game/game.html')

def get_board(request):
    # game = request.session['game']
    board = game.board_str()
    return JsonResponse({'board': board})

def get_moves(request):
    row = int(request.GET.get('row'))
    col = int(request.GET.get('col'))
    square: Piece = game.board[row][col]
    if square:
        return JsonResponse({'moves': square.moves})
    # print(row,col)



