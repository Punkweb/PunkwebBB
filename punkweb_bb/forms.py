from django import forms

from .models import Post, Thread
from .widgets import BBCodeEditor


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
            "content": BBCodeEditor(),
        }
