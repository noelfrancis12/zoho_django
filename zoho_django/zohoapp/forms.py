# forms.py
from django import forms
from django.forms import TextInput,EmailInput

class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email ','style': 'width: 50%;','class':'text-dark'}))
    subject = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Subject','style': 'width: 50%;','class':'text-dark'}))
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
    message = forms.CharField(widget = forms.Textarea(attrs={'placeholder': 'Type messege here........','style': 'width: 50%;','class':'text-dark'}) )