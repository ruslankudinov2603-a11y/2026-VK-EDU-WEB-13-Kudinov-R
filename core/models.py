from django.db import models
from django.contrib.auth.models import User
import uuid

def avatar_upload_path(instance, filename):
    extension = filename.split('.')[-1]
    return f'avatars/{uuid.uuid4()}.{extension}'

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username
