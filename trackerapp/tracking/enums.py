from enum import StrEnum


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
    def display(self) -> str:
        return {
            AnimeRating.G: "Tout âge",
            AnimeRating.PG: "Jeune public",
            AnimeRating.PG13: "13+",
            AnimeRating.R17: "17+ (violence et langage grossier)",
            AnimeRating.RPLUS: "Nudité",
            AnimeRating.RX: "Hentai",
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
    def display(self) -> str:
        return {
            MediaStatus.FINISHED: "Terminé",
            MediaStatus.PUBLISHING: "En cours de publication",
            MediaStatus.HIATUS: "En pause",
            MediaStatus.DISCONTINUED: "Arrêté",
            MediaStatus.NOT_PUBLISHED: "Pas encore sorti",
            # Anime
            MediaStatus.FINISHED_AIRING: "Diffusion terminée",
            MediaStatus.CURRENTLY_AIRING: "En cours de diffusion",
            MediaStatus.NOT_AIRED: "Pas encore diffusé",
        }[self]


class MediaCompletion(StrEnum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

    @property
    def display(self) -> str:
        return {
            MediaCompletion.NOT_STARTED: "Non commencé",
            MediaCompletion.IN_PROGRESS: "En cours",
            MediaCompletion.COMPLETED: "Terminé",
        }[self]
