from django import forms
from django.contrib.auth.models import User
from .models import Board, Card, BoardList
from django.contrib.auth.forms import UserCreationForm


class BoardForm(forms.ModelForm):
    """
    Board Form template
    """

    class Meta:
        model = Board
        fields = ('title',)


class ListForm(forms.ModelForm):
    """
    List Form template
    """

    class Meta:
        model = BoardList
        fields = ('title',)


class CardForm(forms.ModelForm):
    """
    Card Form template
    """

    class Meta:
        model = Card
        fields = ('title',)


class UserForm(forms.Form):
    """
    User form template
    """

    username = forms.CharField(widget=forms.TextInput(), max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100, required=True)
    username.widget.attrs.update({'class':'form-control','placeholder':'Username'})
    password.widget.attrs.update({'class':'form-control','placeholder':'Password'})

    # def clean(self):
    #     cleaned_data = super(UserForm, self).clean()
    #     username = cleaned_data.get('username')
    #     password = cleaned_data.get('password')
    #     if not username and not password:
    #         raise forms.ValidationError('You have to write something!')
    #     # return cleaned_data


class UserSignupForm(forms.ModelForm):

    """
    Sign up form template
    """

    username = forms.CharField(widget=forms.TextInput(), max_length=100, required=True)
    email = forms.EmailField(widget=forms.EmailInput, required=True, label="Email:", max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput(), max_length=100, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), max_length=100, required=True)
    username.widget.attrs.update({'class':'form-control','placeholder':'Username'})
    email.widget.attrs.update({'class':'form-control','placeholder':'Email'})
    password1.widget.attrs.update({'class':'form-control','placeholder':'Password'})
    password2.widget.attrs.update({'class':'form-control','placeholder':'Confirm Password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
    
    def clean(self):
        cleaned_data = super(UserSignupForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if not username and not email and not password1 and not password2:
            raise forms.ValidationError('You have to write something!')
        elif not username:
            raise forms.ValidationError('Please input your username!')
        elif not email:
            raise forms.ValidationError('Please input email!')
        elif password1 != password2:
            raise forms.ValidationError('You input not the same password')
        elif not password1:
            raise forms.ValidationError('Please input your password!')
        else:
            raise forms.ValidationError('Please input your confimation password!')