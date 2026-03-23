from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='profile', verbose_name='Пользователь'
    )
    bio = models.TextField(blank=True, verbose_name='О себе')
    avatar = models.ImageField(
        upload_to='accounts/avatars/', blank=True, null=True,
        verbose_name='Аватар'
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль — {self.user.username}'
