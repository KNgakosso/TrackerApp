from django.db import models

from ..enums import MediaType
from .media_models import MediaModel, SectionCompletion


class AuthorModel(models.Model):
    name = models.CharField()
    mal_id = models.IntegerField()


class MangaModel(MediaModel):
    chapters = models.IntegerField(null=True, blank=True)
    authors = models.ManyToManyField(AuthorModel)

    @property
    def media_type(self):
        return MediaType.MANGA


class VolumeModel(models.Model):
    mal_id = models.IntegerField()
    title = models.CharField(blank=True)
    number = models.IntegerField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    user_score = models.IntegerField(blank=True, null=True)
    user_completion = models.CharField(
        default=SectionCompletion.NOT_STARTED, choices=SectionCompletion
    )
    synopsis = models.CharField(blank=True)
    manga = models.ForeignKey(
        MangaModel, on_delete=models.CASCADE, related_name="volumes"
    )
