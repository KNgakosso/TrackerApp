from django.db import models

from ..domain.enums import AnimeRating
from .media_models import MediaModel, SectionCompletion


class StudioModel(models.Model):
    name = models.CharField()
    mal_id = models.IntegerField()


class AnimeModel(MediaModel):
    studios = models.ManyToManyField(StudioModel)
    duration = models.CharField(blank=True)
    rating = models.CharField(
        blank=True, choices=[(rating.value, rating.display) for rating in AnimeRating]
    )

    def type(self):
        return "anime"


class EpisodeModel(models.Model):
    mal_id = models.IntegerField()
    title = models.CharField(blank=True)
    score = models.FloatField(blank=True, null=True)
    filler = models.BooleanField(default=False)
    recap = models.BooleanField(default=False)
    user_score = models.IntegerField(blank=True, null=True)
    user_completion = models.CharField(
        default=SectionCompletion.NOT_STARTED, choices=SectionCompletion
    )
    synopsis = models.CharField(blank=True)
    anime = models.ForeignKey(
        AnimeModel, on_delete=models.CASCADE, related_name="episodes"
    )
