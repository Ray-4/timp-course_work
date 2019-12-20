import os
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# Профиль создается при регистрации пользователя
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Профиль сохраняется при создании или редактировании.
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# Файл изображения профиля удаляется при удалении профиля.
@receiver(post_delete, sender=Profile)
def auto_delete_profile_image_file_on_profile_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path) and not instance.image.path.endswith("/media/default.jpg"):
            os.remove(instance.image.path)


"""
# Файл изображения профиля удаляется при изменении изображения.
@receiver(pre_save, sender=Profile)
def auto_delete_profile_image_file_on_image_update(sender, instance, **kwargs):
    try:
        old_file = Profile.objects.get(pk=instance.pk).image
    except Profile.DoesNotExist:
        return False

    new_file = instance.image
    if new_file != old_file:
        if os.path.isfile(old_file.path) and not old_file.path.endswith("/media/default.jpg"):
            os.remove(old_file.path)
"""
