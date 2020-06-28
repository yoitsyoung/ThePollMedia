from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    location = forms.CharField(max_length =100)
    bio = forms.CharField(max_length = 200)
    class Meta:
        model = User
        fields = ("username","first_name", "last_name", "email", "location", "bio")


class QuestionForm(forms.ModelForm):
    option_one = forms.CharField(max_length=30)
    option_two = forms.CharField(max_length=30)
    option_three = forms.CharField(max_length=30)
    option_four = forms.CharField(max_length=30)
    class Meta:
        model = Question
        fields = ("title", "content", "option_one", "option_two", "option_three", "option_four")

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ("content",)

QuestionFromSet = forms.formset_factory(OptionForm)


class UserSearchForm(forms.Form):
    username = forms.CharField(max_length=30)
    
    
