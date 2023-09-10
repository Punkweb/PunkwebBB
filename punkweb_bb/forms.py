from django import forms

from .models import BoardProfile, Post, Shout, Thread
from .widgets import BBCodeEditor


class BoardProfileForm(forms.ModelForm):
    class Meta:
        model = BoardProfile
        fields = [
            "image",
            "signature",
        ]
        widgets = {
            "signature": BBCodeEditor(),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": BBCodeEditor(),
        }


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "pw-input"}),
            "content": BBCodeEditor(),
        }


class ShoutForm(forms.ModelForm):
    class Meta:
        model = Shout
        fields = ["content"]
