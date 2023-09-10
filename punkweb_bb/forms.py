from django import forms

from .models import BoardProfile, Post, Shout, Thread
from .widgets import BBCodeEditorWidget


class BoardProfileModelForm(forms.ModelForm):
    class Meta:
        model = BoardProfile
        fields = [
            "image",
            "signature",
        ]
        widgets = {
            "signature": BBCodeEditorWidget(),
        }


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": BBCodeEditorWidget(),
        }


class ThreadModelForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "pw-input"}),
            "content": BBCodeEditorWidget(),
        }


class ShoutModelForm(forms.ModelForm):
    class Meta:
        model = Shout
        fields = ["content"]
