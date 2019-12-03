from django import forms
from .models import Board, Card, BoardList

class BoardForm(forms.ModelForm):
    
    class Meta:
        model = Board
        fields = ('title',)