from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from punkweb_bb.models import BoardProfile, Category, Post, Shout, Subcategory, Thread
from punkweb_bb.utils import get_editor_widget


class LoginForm(AuthenticationForm):
    template_name = "punkweb_bb/forms/stacked_form.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"autofocus": True, "class": "pw-input fluid"}
        )
        self.fields["password"].widget.attrs.update({"class": "pw-input fluid"})


class SignUpForm(UserCreationForm):
    template_name = "punkweb_bb/forms/stacked_form.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"autofocus": True, "class": "pw-input fluid"}
        )
        self.fields["password1"].widget.attrs.update({"class": "pw-input fluid"})
        self.fields["password2"].widget.attrs.update({"class": "pw-input fluid"})


class FilterUsersForm(forms.Form):
    template_name = "punkweb_bb/forms/inline_form.html"

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "pw-input", "placeholder": "Search"}),
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
        widget=forms.Select(attrs={"class": "pw-input"}),
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
            "name": forms.TextInput(attrs={"autofocus": True, "class": "pw-input"}),
            "order": forms.TextInput(
                attrs={"class": "pw-input", "min": "0", "type": "number"}
            ),
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
            "name",
            "description",
            "order",
            "staff_post_only",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"autofocus": True, "class": "pw-input fluid"}
            ),
            "description": get_editor_widget(),
            "order": forms.NumberInput(attrs={"class": "pw-input", "min": "0"}),
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
            "title": forms.TextInput(
                attrs={"autofocus": True, "class": "pw-input fluid"}
            ),
            "content": get_editor_widget(),
        }


class ThreadMoveForm(forms.Form):
    template_name = "punkweb_bb/forms/stacked_form.html"

    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        empty_label="Select a subcategory",
        widget=forms.Select(attrs={"class": "pw-input fluid"}),
    )
