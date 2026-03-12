import time
import asyncio
from asgiref.sync import sync_to_async
from django.http.response import JsonResponse,HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from game.models import Game, Move


async def long_polling_get_board(request, pk):
    game = await sync_to_async(get_object_or_404)(Game, id=pk)
    move_id = request.GET.get("move_id")
    if move_id == 'undefined': 
        return HttpResponseBadRequest()
    move_id = int(move_id)

    if game.status == 'finished':
        print(1)
        return JsonResponse({'game_over': True})
    # # print(game)

    timeout_sec = 10  # sec
    endtime = time.time() + timeout_sec

    while True:

        def get_last_move():
            return Move.objects.filter(game=game, id__gt=move_id).order_by("id").last()
        
        last_move = await sync_to_async(get_last_move)()
        
        def get_is_my_turn():
            return (game.current == 'white' and game.white == request.user) or \
                    (game.current == 'black' and game.black == request.user)

        is_my_turn = await sync_to_async(get_is_my_turn)()
    
        if last_move:
            # print({'move_id': last_move.id})
            return JsonResponse({'move_id': last_move.id, 'is_my_turn': is_my_turn})

        if time.time() > endtime:
            # print({"move_id": None})
            return JsonResponse({"move_id": None, 'is_my_turn': is_my_turn})
        await asyncio.sleep(1)
