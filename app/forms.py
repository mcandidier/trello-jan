from django import forms
from django.contrib.auth.models import User
from .models import Board, Card, BoardList

class BoardForm(forms.ModelForm):
    """
    Board model form
    """

    class Meta:
        model = Board
        fields = ('title',)


class ListForm(forms.ModelForm):
    """
    List model form
    """

    class Meta:
        model = BoardList
        fields = ('title',)


class CardForm(forms.ModelForm):
    """
    Card model form
    """

    class Meta:
        model = Card
        fields = ('title',)

class UserForm(forms.ModelForm):
    """
    User form
    """

    username = forms.CharField(widget=forms.TextInput(), max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    username.widget.attrs.update({'class':'form-control','placeholder':'Enter Username'})
    password.widget.attrs.update({'class':'form-control','placeholder':'Enter Password'})
    class Meta:
        model = User
        fields = ('username','password',)

