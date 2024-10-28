from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from unfold.widgets import (
    BASE_INPUT_CLASSES,
    UnfoldAdminPasswordInput,
)


class UserCreationForm(BaseUserCreationForm):
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs["class"] = " ".join(BASE_INPUT_CLASSES)

        self.fields["last_name"].widget.attrs["class"] = " ".join(BASE_INPUT_CLASSES)

        self.fields["username"].widget.attrs["class"] = " ".join(BASE_INPUT_CLASSES)

        self.fields["email"].widget.attrs["class"] = " ".join(BASE_INPUT_CLASSES)

        self.fields["password1"].widget = UnfoldAdminPasswordInput(
            attrs={"autocomplete": "new-password"}
        )
        self.fields["password2"].widget = UnfoldAdminPasswordInput(
            attrs={"autocomplete": "new-password"}
        )
