from django.contrib import admin

from profiles.models import UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class UserProfileAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        """
        Return a QuerySet of all UserProfiles which are viewable by the current
        user.

        If the current user is a superuser, return all UserProfiles. Otherwise,
        only return UserProfiles for the current user.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        """
        Return True if the current user has permission to change the given
        UserProfile, or if obj is None, return True if the user has permission
        to change any UserProfile.

        A user has permission to change a UserProfile if they are the user
        associated with the UserProfile or if they are a superuser.
        """
        if obj is None:
            return True
        return obj.user == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """
        Return True if the current user has permission to delete the given
        UserProfile, or if obj is None, return True if the user has permission
        to delete any UserProfile.

        A user has permission to delete a UserProfile if they are the user
        associated with the UserProfile or if they are a superuser.
        """
        if obj is None:
            return True
        return obj.user == request.user or request.user.is_superuser


admin.site.register(UserProfile, UserProfileAdmin)


class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        """
        Return the queryset of users for the admin.

        If the requesting user is a superuser, return the complete queryset.
        Otherwise, restrict the queryset to the requesting user's own data.

        Args:
            request: The HTTP request object.

        Returns:
            QuerySet: The filtered queryset of users.
        """

        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    def get_fieldsets(self, request, obj=None):
        """
        Return the fieldsets for the user form.

        If the requesting user is a superuser, return the default fieldsets.
        Otherwise, limit the fieldsets to specific fields for non-superusers.

        Args:
            request: The HTTP request object.
            obj: The object instance, or None if adding a new object.

        Returns:
            A tuple defining fieldsets for the user form.
        """

        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)

        return (
            (
                None,
                {
                    "fields": (
                        "username",
                        "email",
                        "first_name",
                        "last_name",
                        "password",
                    )
                },
            ),
        )

    def get_readonly_fields(self, request, obj=None):
        """
        Return a tuple of field names that should be read-only.

        If the requesting user is a superuser, return the default readonly fields.
        Otherwise, limit the readonly fields to username and email for non-superusers.

        Args:
            request: The HTTP request object.
            obj: The object instance, or None if adding a new object.

        Returns:
            A tuple of field names that should be read-only.
        """
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return ("username", "email")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
