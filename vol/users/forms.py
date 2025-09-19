from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms 
from .models import CustomUser, Team


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'second_name', 'photo')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'photo')


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('title', 'players')
