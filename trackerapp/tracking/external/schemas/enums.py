from enum import StrEnum


class AgeRating(StrEnum):
    G = "G - All Ages"
    PG = "PG - Children"
    PG13 = "PG-13 - Teens 13 or older"
    R17 = "R - 17+ (violence & profanity)"
    RPLUS = "R+ - Mild Nudity"
    RX = "Rx - Hentai"

    @property
    def filter_value(self) -> str:
        return {
            AgeRating.G: "g",
            AgeRating.PG: "pg",
            AgeRating.PG13: "pg13",
            AgeRating.R17: "r17",
            AgeRating.RPLUS: "r",
            AgeRating.RX: "rx",
        }[self]

    @property
    def display(self) -> str:
        return {
            AgeRating.G: "Tout âge",
            AgeRating.PG: "Jeune public",
            AgeRating.PG13: "13+",
            AgeRating.R17: "17+ (violence et langage grossier)",
            AgeRating.RPLUS: "Nudité",
            AgeRating.RX: "Hentai",
        }[self]
