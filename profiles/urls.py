from django.urls import path

from profiles.views import edit_profile_view, profile_view


urlpatterns = [
    path("", profile_view, name="profile"),
    path("edit/", edit_profile_view, name="edit_profile"),
]
