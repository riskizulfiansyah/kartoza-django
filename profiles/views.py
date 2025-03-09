import json
from django.forms import model_to_dict
from django.shortcuts import redirect, render

from profiles.forms import UserProfileForm, UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from profiles.models import UserProfile


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})


@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return render(request, "profile.html", {"error": "Profile does not exist."})

    return render(request, "profile.html", {"profile": profile})


@login_required
def edit_profile_view(request):
    try:
        profile = request.user.profile
        print(dir(UserProfileForm))
        if request.method == "POST":
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect("profile")
        else:
            form = UserProfileForm(request=request, instance=profile)
    except UserProfile.DoesNotExist:
        return render(
            request, "edit_profile.html", {"error": "Profile does not exist."}
        )
    return render(request, "edit_profile.html", {"form": form})


def map_view(request):
    profiles = UserProfile.objects.all()
    locations = []
    for profile in profiles:

        profile_dict = model_to_dict(
            profile,
            fields=[
                "address",
                "city",
                "state",
                "postal_code",
                "country",
                "phone_number",
            ],
        )

        profile_dict["id"] = profile.user.id
        profile_dict["username"] = profile.user.username

        if profile.location:
            location = {
                "x": profile.location.x,
                "y": profile.location.y,
                "profile": profile_dict,
            }
            locations.append(location)

    return render(request, "map.html", {"locations": json.dumps(locations)})
