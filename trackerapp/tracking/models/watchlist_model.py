from django.db import models
from .media_models import MediaModel


class WatchlistModel(models.Model):
    name = models.CharField(unique=True, max_length=20)
    medias = models.ManyToManyField(MediaModel)
    
    def __str__(self) -> str:
        return self.name