from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import DetailView
from .forms import GameForm
# Create your views here.

def games(request):
    objects = Game.active.all()
    return render(request, 'volleyball/games.html', {
        'objects': objects,
    })

def game_info(request, *args, **kwargs):
    game_id = kwargs['pk']
    game = Game.active.get(pk=game_id)
    players = game.players.all()
    return render(request, 'volleyball/game.html', {
        'game': game,
        'players': players,
    })

def join_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.user in game.players.all():
        game.players.remove(request.user)
    else:
        game.players.add(request.user)
    return redirect('game', pk=pk)


def create_game(request):
    if request.user.status == 'B' or request.user.is_superuser:
        if request.method == 'POST':
            form = GameForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('games')
        else:
            form = GameForm()
    else:
        return redirect('games')
    return render(request, 'volleyball/create_game.html', {'form': form})
