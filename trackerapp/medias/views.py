from django.shortcuts import render
from tracking.forms import ScoreForm, SectionNumberForm, WatchlistForm

from .enums import MediaType


def handle_api_errors(view):

    @wraps(view)
    def wrapper(request, *args, **kwargs):

        try:
            return view(request, *args, **kwargs)

        except ExternalApiError:

            return render(
                request,
                "tracking/api_error.html",
                status=503,
            )

    return wrapper


@handle_api_errors
def media_details(request, mal_id: int, media_type: str):
    media = basis.get_or_fetch_media(mal_id, MediaType(media_type))

    return render(
        request,
        "tracking/media_details.html",
        context={
            "media": media,
            "watchlist_selection_form": WatchlistForm(),
            "section_number_form": basis.get_section_number_form(media),
            "score_form": ScoreForm(),
            "show_translation": False,
        },
    )


def translate_synopsis(request, mal_id: int, media_type: str):
    media = use_cases.translate_synopsis(mal_id, MediaType(media_type))
    return render(
        request,
        "tracking/media_details.html",
        context={
            "media": media,
            "watchlist_selection_form": WatchlistForm(),
            "section_number_form": basis.get_section_number_form(media),
            "score_form": ScoreForm(),
            "show_translation": True,
        },
    )
