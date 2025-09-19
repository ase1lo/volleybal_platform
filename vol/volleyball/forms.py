from django import forms
from .models import Game


class DatePickerInput(forms.DateInput):
    input_type = 'date'

class GameForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'uk-input',
            'id': 'form-horizontal-text',
            'type': 'text',
            'name': 'title',
            'value': '',
            'placeholder': 'Some text...',
        })
        self.fields['game_date'].widget.attrs.update({
            'class': 'uk-input',
            'id': 'form-horizontal-text',
            'type': 'text',
            'name': 'title',
            'value': '',
            'placeholder': 'Some text...',
        })
        self.fields['status'].widget.attrs.update({
           'class': 'uk-input',
            'id': 'form-horizontal-text',
            'type': 'text',
            'name': 'title',
            'value': '',
            'placeholder': 'Some text...',
        })
        self.fields['adress'].widget.attrs.update({
           'class': 'uk-input',
            'id': 'form-horizontal-text',
            'type': 'text',
            'name': 'title',
            'value': '',
            'placeholder': 'Точный адрес',
        })

    class Meta:
        model = Game
        fields = ('title', 'game_date', 'status', 'adress')
        widgets = {
            'game_date': DatePickerInput(),
        }