from django import forms

from punkweb_bb.models import BoardProfile, Category, Post, Subcategory, Thread
from punkweb_bb.widgets import BBCodeEditorWidget


class BoardProfileAdminModelForm(forms.ModelForm):
    class Meta:
        model = BoardProfile
        fields = "__all__"
        widgets = {
            "signature": BBCodeEditorWidget(),
        }


class CategoryAdminModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "description": BBCodeEditorWidget(),
        }


class SubcategoryAdminModelForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = "__all__"
        widgets = {
            "description": BBCodeEditorWidget(),
        }


class ThreadAdminModelForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = "__all__"
        widgets = {
            "content": BBCodeEditorWidget(),
        }


class PostAdminModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            "content": BBCodeEditorWidget(),
        }
