from django import forms

from profiles.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from leaflet.forms.widgets import LeafletWidget


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
        widgets = {
            "location": LeafletWidget(attrs={"zoom": 15}),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if request and not request.user.is_superuser:
            self.fields["user"].widget = forms.HiddenInput()
        if self.instance.location:
            self.fields["location"].widget.attrs["initial"] = self.instance.location


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
