from django import forms
from .models import Board, Card, BoardList

class BoardForm(forms.ModelForm):

    class Meta:
        model = Board
        fields = ('title',)


class ListForm(forms.ModelForm):

    class Meta:
        model = BoardList
        fields = ('title',)


class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        fields = ('title',)