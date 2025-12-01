from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from punkweb_bb.models import BoardProfile, Category, Post, Shout, Subcategory, Thread
from punkweb_bb.utils import get_editor_widget


class LoginForm(AuthenticationForm):
    template_name = "punkweb_bb/forms/stacked_form.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"autofocus": True, "class": "w-full"}
        )
        self.fields["password"].widget.attrs.update({"class": "w-full"})


class SignUpForm(UserCreationForm):
    template_name = "punkweb_bb/forms/stacked_form.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"autofocus": True, "class": "w-full"}
        )
        self.fields["password1"].widget.attrs.update({"class": "w-full"})
        self.fields["password2"].widget.attrs.update({"class": "w-full"})


class FilterUsersForm(forms.Form):
    template_name = "punkweb_bb/forms/inline_form.html"

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
    )
    sort_by = forms.ChoiceField(
        required=False,
        choices=(
            ("", "-----------"),
            ("username", "Username (A-Z)"),
            ("-username", "Username (Z-A)"),
            ("date_joined", "Date Joined (Oldest)"),
            ("-date_joined", "Date Joined (Newest)"),
        ),
    )


class BoardProfileModelForm(forms.ModelForm):
    template_name = "punkweb_bb/forms/stacked_form.html"

    class Meta:
        model = BoardProfile
        fields = (
            "image",
            "bio",
            "signature",
        )
        widgets = {
            "bio": get_editor_widget(),
            "signature": get_editor_widget(),
        }


class CategoryModelForm(forms.ModelForm):
    template_name = "punkweb_bb/forms/stacked_form.html"

    class Meta:
        model = Category
        fields = (
            "name",
            "order",
        )
        widgets = {
            "name": forms.TextInput(attrs={"autofocus": True}),
        }


class PostModelForm(forms.ModelForm):
    template_name = "punkweb_bb/forms/stacked_form.html"

    class Meta:
        model = Post
        fields = ("content",)
        labels = {
            "content": "",
        }
        widgets = {
            "content": get_editor_widget(),
        }


class ShoutModelForm(forms.ModelForm):
    class Meta:
        model = Shout
        fields = ("content",)


class SubcategoryModelForm(forms.ModelForm):
    template_name = "punkweb_bb/forms/stacked_form.html"

    class Meta:
        model = Subcategory
        fields = (
            "category",
            "name",
            "description",
            "order",
            "staff_post_only",
        )
        widgets = {
            "name": forms.TextInput(attrs={"autofocus": True, "class": "w-full"}),
            "category": forms.Select(attrs={"class": "w-full"}),
            "description": get_editor_widget(),
            "order": forms.NumberInput(attrs={"min": "0"}),
        }


class ThreadModelForm(forms.ModelForm):
    template_name = "punkweb_bb/forms/stacked_form.html"

    class Meta:
        model = Thread
        fields = (
            "title",
            "content",
        )
        widgets = {
            "title": forms.TextInput(attrs={"autofocus": True, "class": "w-full"}),
            "content": get_editor_widget(),
        }


class ThreadMoveForm(forms.Form):
    template_name = "punkweb_bb/forms/stacked_form.html"

    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        empty_label="Select a subcategory",
        widget=forms.Select(attrs={"class": "w-full"}),
    )
