from django.shortcuts import render
from django.http.response import JsonResponse
from game.chess_board import GameBoard
from game.models import Game
from game.chess_pieces import Piece
import json
# from .models import Game  # если у тебя есть модель Game


# Create your views here.
def create_game(request):
    game_board = GameBoard()
    game=Game(board=json.dumps(game_board.searialize_board()))
    game.save()
    return render(request, "game/index.html", context={'game_id':game.id})


def get_board(request,pk):
    game = Game.objects.get(id=pk)
    game_obj = GameBoard(new_game=False, board_str=game.board)
    return JsonResponse({"board": game_obj.board_str()})



def get_moves(request,pk):
    game = Game.objects.get(id=pk)
    game_obj = GameBoard(new_game=False, board_str=game.board)

    row = int(request.GET.get("row"))
    col = int(request.GET.get("col"))

    square: Piece = game_obj.board[row][col]
    if square:
        square.calc_attack_moves()  # Добавлено
        game.clean_attack_moves(square)  # Добавлено
        return JsonResponse({"moves": square.moves})
    return JsonResponse({"moves": [], "error": "No piece at this position"})

def move_figure(request):
    """3) Надо сделать так, чтобы при тыке на разрешенный ход кидался запрос move_figure"""
    from_row = int(request.GET.get("from_row"))
    from_col = int(request.GET.get("from_col"))
    to_row = int(request.GET.get("to_row"))
    to_col = int(request.GET.get("to_col"))

    # Get the piece and try to move it
    try:
        success = game.move_figure(
            from_row, from_col, to_row, to_col
        )  # кладем результат в суцес и если ок, возвращаем
        game.calc_attack_map("white")
        game.calc_attack_map("black")
        return JsonResponse({"success": success})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    

