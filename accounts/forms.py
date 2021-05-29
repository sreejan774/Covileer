from django import forms
from django.forms import widgets
from django.forms.widgets import PasswordInput 

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'User Name'}))
    password = forms.CharField(widget=PasswordInput)
    confirmPassword = forms.CharField(widget=PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'User Name'}))
    password = forms.CharField(widget=PasswordInput)

class ProfileForm(forms.Form):
    name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'User Name'}))
    contact = forms.CharField(max_length=17,widget=forms.TextInput(attrs={'placeholder': 'Contact'}))
    address = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    city = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'City'}))
    state = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'State'}))
    pincode = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder': 'Pincode'}))