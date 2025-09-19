from .views import *
from django.urls import path, include


urlpatterns = [
    path('games', GamesListAPI.as_view(), name='api_games'),
    path('game/<int:pk>', GameDetailAPI.as_view(), name='api_game'),
    path('user/<int:pk>', UserDetailAPI.as_view(), name='api_user')
]
