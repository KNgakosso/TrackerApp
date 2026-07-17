from django.db import models

from .media_models import MediaModel, SectionCompletion


class StudioModel(models.Model):
    name = models.CharField()
    mal_id = models.IntegerField()


class AnimeModel(MediaModel):
    studios = models.ManyToManyField(StudioModel)
    rating = models.CharField(blank=True)
    number_episodes = models.IntegerField(null=True, blank=True)
    number_seasons = models.IntegerField(null=True, blank=True)

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
