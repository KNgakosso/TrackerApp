from typing import ClassVar

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

from ..tracking.enums import MediaCompletion
from ..tracking.models.media_models import MediaModel

# Create your models here.


class MediaUserInfo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medias_user_info",
    )
    media = models.ForeignKey(
        MediaModel,
        on_delete=models.CASCADE,
        related_name="medias_user_info",
    )
    score = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
    )
    completion = models.CharField(
        default=MediaCompletion.NOT_STARTED,
        choices=[
            (completion.value, completion.display) for completion in MediaCompletion
        ],
    )
    current_section = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
        ],
    )

    class Meta:
        constraints: ClassVar[list] = [
            models.CheckConstraint(
                condition=Q(user_score__gte=0) & Q(user_score__lte=10),
                name="user_score_between_0_and_10",
            ),
            models.UniqueConstraint(fields=["user", "media"], name="unique_user_media"),
        ]
