from django import forms

from .models import BoardProfile, Category, Post, Subcategory, Thread
from .widgets import BBCodeEditorWidget


class BoardProfileAdminForm(forms.ModelForm):
    class Meta:
        model = BoardProfile
        fields = "__all__"
        widgets = {
            "signature": BBCodeEditorWidget(),
        }


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "description": BBCodeEditorWidget(),
        }


class SubcategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = "__all__"
        widgets = {
            "description": BBCodeEditorWidget(),
        }


class ThreadAdminForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = "__all__"
        widgets = {
            "content": BBCodeEditorWidget(),
        }


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            "content": BBCodeEditorWidget(),
        }
