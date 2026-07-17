from django.db import models
from polymorphic.models import PolymorphicModel


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


class MediaModelStatus(models.TextChoices):
    NOT_STARTED = "not_started", "Non commencé"
    IN_PROGRESS = "in_progress", "En cours"
    COMPLETED = "completed", "Terminé"


class MediaModel(PolymorphicModel):
    mal_id = models.IntegerField()
    title = models.CharField()
    user_score = models.IntegerField(null=True, blank=True)
    user_completion = models.CharField(
        default=MediaModelStatus.NOT_STARTED, choices=MediaModelStatus
    )
    user_current_section = models.IntegerField(null=True, blank=True)

    score = models.FloatField(null=True, blank=True)
    synopsis = models.CharField(blank=True)
    number_sections = models.IntegerField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    status = models.CharField(blank=True)
    themes = models.ManyToManyField(ThemeModel)
    genres = models.ManyToManyField(GenreModel)
    demographics = models.ManyToManyField(DemographicModel)

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


class ImagesModel(models.Model):
    media = models.OneToOneField(
        MediaModel, on_delete=models.CASCADE, related_name="images"
    )
    small_image_url = models.CharField(blank=True)
    medium_image_url = models.CharField(blank=True)
    large_image_url = models.CharField(blank=True)


class SectionCompletion(models.TextChoices):
    NOT_STARTED = "not_started", "Non commencé"
    COMPLETED = "completed", "Terminé"
