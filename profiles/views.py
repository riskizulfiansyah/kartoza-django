from django.shortcuts import redirect, render

from profiles.forms import UserRegistrationForm
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
