from django import forms
from django.contrib.auth.models import User
from .models import Board, Card, BoardList
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

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

class UserForm(forms.ModelForm):
    """
    User form
    """

    username = forms.CharField(widget=forms.TextInput(), max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    username.widget.attrs.update({'class':'form-control','placeholder':'Username'})
    password.widget.attrs.update({'class':'form-control','placeholder':'Password'})
    class Meta:
        model = User
        fields = ('username','password',)

class UserSignupForm(forms.ModelForm):
    """
    Create user
    """

    username = forms.CharField(widget=forms.TextInput(), max_length=100)
    email = forms.EmailField(widget=forms.EmailInput, required=False, label="Email:", max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    username.widget.attrs.update({'class':'form-control','placeholder':'Username'})
    email.widget.attrs.update({'class':'form-control','placeholder':'Email'})
    password1.widget.attrs.update({'class':'form-control','placeholder':'Password'})
    password2.widget.attrs.update({'class':'form-control','placeholder':'Confirm Password'})
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

