from enum import StrEnum

from django.utils.translation import gettext_lazy as _


class MediaType(StrEnum):
    ANIME = "anime"
    MANGA = "manga"


class AnimeRating(StrEnum):
    G = "G - All Ages"
    PG = "PG - Children"
    PG13 = "PG-13 - Teens 13 or older"
    R17 = "R - 17+ (violence & profanity)"
    RPLUS = "R+ - Mild Nudity"
    RX = "Rx - Hentai"

    @property
    def filter_value(self) -> str:
        return {
            AnimeRating.G: "g",
            AnimeRating.PG: "pg",
            AnimeRating.PG13: "pg13",
            AnimeRating.R17: "r17",
            AnimeRating.RPLUS: "r",
            AnimeRating.RX: "rx",
        }[self]

    @property
    def display(self):
        return {
            AnimeRating.G: _("All ages"),
            AnimeRating.PG: _("Young audience"),
            AnimeRating.PG13: _("13+"),
            AnimeRating.R17: _("Violence and profanity"),
            AnimeRating.RPLUS: _("Mild Nudity"),
            AnimeRating.RX: _("Hentai"),
        }[self]


class MediaStatus(StrEnum):
    # Manga
    FINISHED = "Finished"
    PUBLISHING = "Publishing"
    HIATUS = "On Hiatus"
    DISCONTINUED = "Discontinued"
    NOT_PUBLISHED = "Not yet published"
    # Anime
    FINISHED_AIRING = "Finished Airing"
    CURRENTLY_AIRING = "Currently Airing"
    NOT_AIRED = "Not yet aired"

    @property
    def filter_value(self) -> str:
        return {
            # Manga
            MediaStatus.FINISHED: "complete",
            MediaStatus.PUBLISHING: "publishing",
            MediaStatus.HIATUS: "hiatus",
            MediaStatus.DISCONTINUED: "discontinued",
            MediaStatus.NOT_PUBLISHED: "upcoming",
            # Anime
            MediaStatus.FINISHED_AIRING: "complete",
            MediaStatus.CURRENTLY_AIRING: "airing",
            MediaStatus.NOT_AIRED: "upcoming",
        }[self]

    @property
    def display(self):
        return {
            MediaStatus.FINISHED: _("Finished"),
            MediaStatus.PUBLISHING: _("Currently publishing"),
            MediaStatus.HIATUS: _("On hiatus"),
            MediaStatus.DISCONTINUED: _("Discontinued"),
            MediaStatus.NOT_PUBLISHED: _("Not yet published"),
            # Anime
            MediaStatus.FINISHED_AIRING: _("Finished airing"),
            MediaStatus.CURRENTLY_AIRING: _("Currently airing"),
            MediaStatus.NOT_AIRED: _("Not yet aired"),
        }[self]


class MediaCompletion(StrEnum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

    @property
    def display(self):
        return {
            MediaCompletion.NOT_STARTED: _("Not started"),
            MediaCompletion.IN_PROGRESS: _("In progress"),
            MediaCompletion.COMPLETED: _("Completed"),
        }[self]
