from typing import ClassVar

from django.conf import settings
from django.db import models
from medias.models.media_models import MediaModel


class WatchlistModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    medias = models.ManyToManyField(MediaModel)

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints: ClassVar[list] = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_user_watchlist_name"
            ),
        ]
