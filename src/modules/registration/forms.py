from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django import forms
from django.contrib.auth.models import User

from unfold.widgets import (
    BASE_INPUT_CLASSES,
    UnfoldAdminPasswordInput,
)


class UserCreationForm(BaseUserCreationForm):
    first_name = forms.CharField(label="First name", max_length=100)
    last_name = forms.CharField(label="Last name", max_length=100)
    email = forms.EmailField(label="Email", max_length=100)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field_name in ["first_name", "last_name", "username", "email"]:
            self.fields[field_name].widget.attrs["class"] = " ".join(BASE_INPUT_CLASSES)

        self.fields["password1"].widget = UnfoldAdminPasswordInput(
            attrs={"autocomplete": "new-password"}
        )
        self.fields["password2"].widget = UnfoldAdminPasswordInput(
            attrs={"autocomplete": "new-password"}
        )
