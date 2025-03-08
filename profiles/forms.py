from django import forms

from profiles.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "user",
            "address",
            "city",
            "state",
            "postal_code",
            "country",
            "phone_number",
            "location",
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if request and not request.user.is_superuser:
            self.fields["user"].widget = forms.HiddenInput()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
