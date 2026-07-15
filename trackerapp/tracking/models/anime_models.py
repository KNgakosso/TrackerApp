from django.db import models
from .media_models import MediaModel

class StudioModel(models.Model):
    name = models.CharField()
    mal_id = models.IntegerField()

class AnimeModel(MediaModel):
    studios = models.ManyToManyField(StudioModel)
    rating = models.CharField()
    number_episodes = models.IntegerField(null=True, blank=True)
    number_seasons = models.IntegerField(null=True, blank=True)

    def type(self):
        return "anime"

class EpisodeModel(models.Model):
    mal_id = models.IntegerField()
    title = models.CharField()
    score = models.FloatField()
    filler = models.BooleanField()
    recap = models.BooleanField()
    user_score = models.IntegerField()
    user_completion_choices = [
        ('Finished', 'Finished'),
        ('Unseen', 'Unseen')
    ]
    user_completion = models.CharField(default = 'Unseen', choices=user_completion_choices)
    synopsis = models.CharField()
    anime = models.ForeignKey(
        AnimeModel,
        on_delete=models.CASCADE,
        related_name="episodes"
    )    