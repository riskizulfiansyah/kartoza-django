from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission
from django.dispatch import receiver
from django.db.models.signals import post_save

from profiles.models import UserProfile


@receiver(post_save, sender=User)
def setup_user_permissions(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        instance.is_staff = True

        user_content_type = ContentType.objects.get_for_model(User)

        view_user_perm = Permission.objects.get(
            content_type=user_content_type, codename="view_user"
        )
        change_user_perm = Permission.objects.get(
            content_type=user_content_type, codename="change_user"
        )

        instance.user_permissions.add(view_user_perm)
        instance.user_permissions.add(change_user_perm)

        user_profile_content_type = ContentType.objects.get_for_model(UserProfile)

        view_user_profile_perm = Permission.objects.get(
            content_type=user_profile_content_type, codename="view_userprofile"
        )
        change_user_profile_perm = Permission.objects.get(
            content_type=user_profile_content_type, codename="change_userprofile"
        )

        instance.user_permissions.add(view_user_profile_perm)
        instance.user_permissions.add(change_user_profile_perm)

        instance.save()
