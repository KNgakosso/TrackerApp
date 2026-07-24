from django.db import models
from polymorphic.models import PolymorphicModel

from ..domain.enums import MediaCompletion, MediaStatus


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
    small_image_url = models.CharField(blank=True)
    image_url = models.CharField(blank=True)
    large_image_url = models.CharField(blank=True)

    score = models.FloatField(null=True, blank=True)
    synopsis = models.CharField(blank=True)
    number_sections = models.IntegerField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        choices=[(status.value, status.display) for status in MediaStatus]
    )
    themes = models.ManyToManyField(ThemeModel)
    genres = models.ManyToManyField(GenreModel)
    demographics = models.ManyToManyField(DemographicModel)
    user_score = models.IntegerField(null=True, blank=True)
    user_completion = models.CharField(
        default=MediaCompletion.NOT_STARTED,
        choices=[
            (completion.value, completion.display) for completion in MediaCompletion
        ],
    )
    user_current_section = models.IntegerField(null=True, blank=True)

    def type(self):
        raise NotImplementedError


"""
class RelationModel(models.Model):
    origin_media = models.ForeignKey(
        MediaModel,
        on_delete=models.CASCADE,
        related_name="relations"
    )
    relation_type = models.CharField()
    name = models.CharField(blank=True)
    image_url = models.CharField(blank=True)
    media_type = models.CharField(blank=True)
"""


class SectionCompletion(models.TextChoices):
    NOT_STARTED = "not_started", "Non commencé"
    COMPLETED = "completed", "Terminé"
