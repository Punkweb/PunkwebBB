from django import forms

from punkweb_bb.models import (
    BoardProfile,
    Category,
    GroupStyle,
    Post,
    Subcategory,
    Thread,
)
from punkweb_bb.utils import get_editor_widget
from punkweb_bb.widgets import BBCodeEditorWidget


class BoardProfileAdminModelForm(forms.ModelForm):
    class Meta:
        model = BoardProfile
        fields = "__all__"
        widgets = {
            "signature": get_editor_widget(),
        }


class CategoryAdminModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "description": get_editor_widget(),
        }


class SubcategoryAdminModelForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = "__all__"
        widgets = {
            "description": get_editor_widget(),
        }


class ThreadAdminModelForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = "__all__"
        widgets = {
            "content": get_editor_widget(),
        }


class PostAdminModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            "content": get_editor_widget(),
        }


class GroupStyleAdminModelForm(forms.ModelForm):
    class Meta:
        model = GroupStyle
        fields = "__all__"
        widgets = {
            "username_style": BBCodeEditorWidget(),
        }
