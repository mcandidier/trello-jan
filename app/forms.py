from django import forms
from django.contrib.auth.models import User
from .models import Board, Card, BoardList
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email


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


class UserSignupForm(forms.ModelForm):
    """
    Sign up form template
    """

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # validate if p1 and p2 is equal
        if password1 != password2:
            # if p1 and p2 is not the same it will raise error
            raise forms.ValidationError('Password and confirm password does not match!')
        return

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use!')