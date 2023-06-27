from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from django import forms
from django.contrib.auth.models import User
from .models import *




class CreateUserForm(UserCreationForm):
    matricule = forms.CharField(max_length=200 , required=True)
    email = forms.CharField(max_length=50)
    class Meta : 
        model = User
        fields = UserCreationForm.Meta.fields + ('matricule','email',)