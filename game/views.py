from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from game.chess_board import GameBoard
from game.models import Game, Move
from game.chess_pieces import Piece
import json
import random



# Create your views here.
def create_game(request):
    color = request.POST.get('color')
    print("ПОЛУЧЕН ЦВЕТ:", color)
    
    if not color:
        return redirect('main:lobby')
    game_obj = GameBoard()
    game=Game(board=json.dumps(game_obj.searialize_board()))
    if color == 'white':
        game.white = request.user
    elif color == 'black':
        game.black = request.user
    if color == 'random':
        result = bool(random.getrandbits(1))
        print(result)
        if result:
            game.white = request.user
        else:
            game.black = request.user

    game.save()
    print(1)
    return redirect('game:render_game', pk=game.id)

    
def render_game(request, pk):
    game = Game.objects.get(id=pk)
    user = request.user
    if not game:  
        return redirect('main:lobby')
    color = 'white' if game.white == request.user else 'black'
    return render(request, "game/index.html", context={'game_id':pk, 'color': color})

@login_required
def join_game(request):
    id = request.GET.get('id')
    if not id:
        return redirect('main:lobby')
    game=Game.objects.get(id=id)
    if not game: 
        return redirect('main:lobby')
    


    if game.white and not game.black:
        game.black = request.user
    elif game.black and not game.white:
        game.white = request.user
    elif request.user == game.black or request.user == game.white:
        pass
    else: 
        return redirect('main:lobby')
    game.save()
    
    return redirect('game:render_game', pk=game.id)

def get_board(request,pk):
    game = Game.objects.get(id=pk)
    game_obj = GameBoard(new_game=False, board_str=game.board, current=game.current)
    return JsonResponse({"board": game_obj.board_str_func()})


def get_moves(request,pk):
    game = Game.objects.get(id=pk)
    game_obj = GameBoard(new_game=False, board_str=game.board, current=game.current)

    row = int(request.GET.get("row"))
    col = int(request.GET.get("col"))

    square: Piece = game_obj.board[row][col]
    if square:
        return JsonResponse({"moves": square.moves})
    return JsonResponse({"moves": [], "error": "No piece at this position"})

def move_figure(request,pk):
    """3) Надо сделать так, чтобы при тыке на разрешенный ход кидался запрос move_figure"""
    from_row = int(request.GET.get("from_row"))
    from_col = int(request.GET.get("from_col"))
    to_row = int(request.GET.get("to_row"))
    to_col = int(request.GET.get("to_col"))

    
    game = Game.objects.get(id=pk)
    if game.current == 'white' and game.white != request.user: #почему проверка только у белого?
        return JsonResponse({"success": False})
    elif game.current == 'black' and game.black != request.user: 
        return JsonResponse({"success": False})
    game_obj = GameBoard(new_game=False, board_str=game.board, current=game.current)   


    # Get the piece and try to move it
    status = game_obj.move_figure(
        from_row, from_col, to_row, to_col
    )  # кладем результат в суцес и если ок, возвращаем
    if status in ['success', 'pawn_promotion'] :
        move = Move(game = game, user = request.user, index = 'e5')
        move.save()
        
        a = game_obj.searialize_board()
        game.board = json.dumps(a)
        game.save()
        if status == 'success':
            game_obj.calc_attack_map("white")
            print("calc map succes w")
            game_obj.calc_attack_map("black")
            print("calc map succes b")
            current = 'white' if game.current == 'black' else 'black'
            print(a)
            game.current = current
            game.save()
            return JsonResponse({"success": True, 'from_row': from_row, 'from_col':from_col, 'to_row': to_row, 'to_col': to_col})
        else:
            return JsonResponse({"success": True, 'message': 'pawn_promotion', 'from_row': from_row, 'from_col': from_col, 'to_row': to_row, 'to_col': to_col})
    return JsonResponse({"success": False, "error": status})
    
def pawn_promotion(request, pk):
    piece = request.GET.get("piece")
    row = int(request.GET.get("row"))
    col = int(request.GET.get("col"))
    
    game = Game.objects.get(id=pk)
    game_obj = GameBoard(new_game=False, board_str=game.board, current=game.current)
    game_obj.pawn_promotion(piece, row, col)
    

    a = game_obj.searialize_board()
    game.board = json.dumps(a)
    current = 'white' if game.current == 'black' else 'black'
    game.current = current
    game.save()

    return JsonResponse({"success": True})


def long_polling_get_board(request, pk):
    pass    