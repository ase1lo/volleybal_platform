from rest_framework import serializers
from volleyball.models import Game
from users.models import CustomUser

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'game_date',
            'adress',
            'players',
        )
        model = Game
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'first_name',
            'second_name',
            'email',
            'rating',
            'status',
            'photo',
        )
        model = CustomUser