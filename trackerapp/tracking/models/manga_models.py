from django.db import models
from .media_models import MediaModel

class AuthorModel(models.Model):
    name = models.CharField()
    mal_id = models.IntegerField()

class MangaModel(MediaModel):
    authors = models.ManyToManyField(AuthorModel)
    number_volumes = models.IntegerField(null=True, blank=True)

    def type(self):
        return "manga"
    
class VolumeModel(models.Model):
    mal_id  = models.IntegerField()
    title = models.CharField()
    number = models.IntegerField()
    score = models.FloatField()
    user_score = models.IntegerField()
    user_completion_choices = [
        ('Finished', 'Finished'),
        ('Unseen', 'Unseen')
    ]
    user_completion = models.CharField(default = 'Unseen', choices=user_completion_choices)
    synopsis = models.CharField()
    manga = models.ForeignKey(
        MangaModel,
        on_delete=models.CASCADE,
        related_name="volumes"
    )