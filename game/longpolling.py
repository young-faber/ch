import time
import asyncio
from asgiref.sync import sync_to_async
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from game.models import Game, Move


async def long_polling_get_board(request, pk):
    game = await sync_to_async(get_object_or_404)(Game, id=pk)

    move_id = int(request.GET.get("move_id"))

    print(game)

    timeout_sec = 10  # sec
    endtime = time.time() + timeout_sec
    while True:

        def get_last_move():
            return Move.objects.filter(game=game, id__gt=move_id).order_by("id").last()
        
        last_move = await sync_to_async(get_last_move)()
        print('LAST', last_move)

        if last_move:
            return JsonResponse({'move_id': last_move.id})

        if time.time() > endtime:
            return JsonResponse({"move_id": None})
        await asyncio.sleep(1)
