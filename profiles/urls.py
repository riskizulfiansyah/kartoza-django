from django.urls import path

from profiles.views import profile_view


urlpatterns = [
    path("", profile_view, name="profile"),
]
