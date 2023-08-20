from django import forms

from .models import BoardProfile, Category, Post, Subcategory, Thread
from .widgets import BBCodeEditor


class BoardProfileAdminForm(forms.ModelForm):
    class Meta:
        model = BoardProfile
        fields = "__all__"
        widgets = {
            "signature": BBCodeEditor(),
        }


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "description": BBCodeEditor(),
        }


class SubcategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = "__all__"
        widgets = {
            "description": BBCodeEditor(),
        }


class ThreadAdminForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = "__all__"
        widgets = {
            "content": BBCodeEditor(),
        }


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            "content": BBCodeEditor(),
        }
