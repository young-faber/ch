from django.shortcuts import render
from django.http.response import JsonResponse
from game.chess_board import Game
from game.chess_pieces import Piece
# from .models import Game  # если у тебя есть модель Game

game = Game()
game.calc_attack_map('white')
game.calc_attack_map('black')

# Create your views here.
def create_game(request):
    # request.session['game'] = game
    return render(request, 'game/index.html')

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

def move_figure(request):
    '''3) Надо сделать так, чтобы при тыке на разрешенный ход кидался запрос move_figure'''
    from_row = int(request.GET.get('from_row'))
    from_col = int(request.GET.get('from_col'))
    to_row = int(request.GET.get('to_row'))
    to_col = int(request.GET.get('to_col'))

    # Get the piece and try to move it
    try:
        success = game.move_figure(from_row, from_col, to_row, to_col)
        game.calc_attack_map('white')
        game.calc_attack_map('black')
        return JsonResponse({'success': success})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

    # game.calc_attack_map('white')
    # game.calc_attack_map('black')
    

