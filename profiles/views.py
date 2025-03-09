import json
from django.forms import model_to_dict
from django.shortcuts import redirect, render

from profiles.forms import UserProfileForm, UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from profiles.models import UserProfile


def register(request):
    """
    Handle user registration.

    If the request method is POST, validate and register a new user using the UserRegistrationForm.
    If the form is valid, log the user in and redirect them to their profile page.
    If the request method is not POST, display an empty registration form.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered registration page with the form.
    """

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
    """
    Display the user's profile.

    If the user has a profile, display their profile page.
    If the user does not have a profile, display an error message.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered profile page.
    """
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        return render(request, "profile.html", {"error": "Profile does not exist."})

    return render(request, "profile.html", {"profile": profile})


@login_required
def edit_profile_view(request):
    """
    Edit the user's profile.

    If the request method is POST, validate and save the user's profile data using the UserProfileForm.
    If the form is valid, save the changes and redirect the user to their profile page.
    If the request method is not POST, display the user's current profile data in the form.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered edit profile page with the form or an error message if the profile does not exist.
    """

    try:
        profile = request.user.profile
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
    """
    Display a map with user locations.

    Query all user profiles from the database and serialize their location data.
    Render a map with Leaflet.js and add markers for each user profile with a location.
    The marker tooltip displays the user's username and the marker popup displays their address,
    city, state, postal code, country, and phone number.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered map page with the user location markers.
    """
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
