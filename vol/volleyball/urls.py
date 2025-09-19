from django.urls import path, include
from .views import *
urlpatterns = [
    path('', games, name='games'),
    path('game/<int:pk>', game_info, name='game'),
    path('game/<int:pk>/join', join_game, name='join_game'),
    path('create_game', create_game, name='create_game')
]
