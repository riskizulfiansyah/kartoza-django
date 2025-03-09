from django.contrib import admin

from profiles.models import UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class UserProfileAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.user == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.user == request.user or request.user.is_superuser


admin.site.register(UserProfile, UserProfileAdmin)


class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    def get_fieldsets(self, request, obj=None):
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
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return ("username", "email")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
