from django.db import models
from polymorphic.models import PolymorphicModel

from ..enums import MediaStatus, MediaType


class GenreModel(models.Model):
    name = models.CharField(unique=True)
    mal_id_anime = models.IntegerField(null=True)
    mal_id_manga = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.name


class DemographicModel(models.Model):
    name = models.CharField(unique=True)
    mal_id_anime = models.IntegerField(null=True)
    mal_id_manga = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.name


class ThemeModel(models.Model):
    name = models.CharField(unique=True)
    mal_id_anime = models.IntegerField(null=True)
    mal_id_manga = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.name


class MediaModel(PolymorphicModel):
    mal_id = models.IntegerField()
    title = models.CharField()
    title_english = models.CharField(blank=True)
    title_french = models.CharField(blank=True)
    small_image_url = models.CharField(blank=True)
    image_url = models.CharField(blank=True)
    large_image_url = models.CharField(blank=True)
    format = models.CharField(blank=True)
    score = models.FloatField(null=True, blank=True)
    synopsis = models.CharField(blank=True)
    synopsis_translated = models.CharField(blank=True)
    number_sections = models.IntegerField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        blank=True, choices=[(status.value, status.display) for status in MediaStatus]
    )
    themes = models.ManyToManyField(ThemeModel)
    genres = models.ManyToManyField(GenreModel)
    demographics = models.ManyToManyField(DemographicModel)

    @property
    def media_type(self) -> MediaType:
        raise NotImplementedError
