from django import forms

class BoardForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
