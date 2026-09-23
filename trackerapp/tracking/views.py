from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from medias.enums import MediaType
from research.forms import SearchForm
from watchlists.forms import WatchlistSelectionForm

from .exceptions import ExternalApiError
from .forms import ScoreForm, SectionNumberForm
from .services.storage import storage_services
from .use_cases import basis, use_cases


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


@login_required
def index(request):
    return render(
        request,
        "tracking/index.html",
        context={
            "watchlists": storage_services.get_watchlists(user=request.user),
            "search_form": SearchForm(),
            "medias": basis.get_ongoing_medias(user=request.user),
        },
    )


def finished_medias(request):
    medias = basis.get_finished_medias()
    return render(request, "tracking/finished_medias.html", context={"medias": medias})


def complete_media_next_section(request, mal_id: int, media_type: str):
    media = use_cases.complete_media_next_section(mal_id, MediaType(media_type))
    return redirect(request.POST.get("next", "tracking:media_details"))


def complete_media_section(request, mal_id: int, media_type: str):
    if request.method == "POST":
        section_number_form = SectionNumberForm(request.POST)
        if section_number_form.is_valid():
            media = use_cases.set_media_current_user_section(
                mal_id, MediaType(media_type), section_number_form
            )
            return render(
                request,
                "tracking/media_details.html",
                context={
                    "media": media,
                    "watchlist_selection_form": WatchlistSelectionForm(
                        user=request.user
                    ),
                    "section_number_form": basis.get_section_number_form(media),
                    "score_form": ScoreForm(),
                },
            )

    return redirect("tracking:media_details", mal_id=mal_id, media_type=media_type)


@login_required
def set_media_user_score(request, mal_id: int, media_type: str):
    if request.method == "POST":
        score_form = ScoreForm(request.POST)
        if score_form.is_valid():
            media = use_cases.set_media_user_score(
                mal_id, MediaType(media_type), score_form
            )
            return render(
                request,
                "tracking/media_details.html",
                context={
                    "media": media,
                    "watchlist_selection_form": WatchlistSelectionForm(
                        user=request.user
                    ),
                    "section_number_form": basis.get_section_number_form(media),
                    "score_form": ScoreForm(),
                },
            )
    else:
        score_form = ScoreForm()
    return render(
        request,
        "tracking/index.html",
        context={
            "watchlists": storage_services.get_watchlists(user=request.user),
            "search_form": SearchForm(),
            "medias": basis.get_ongoing_medias(),
        },
    )


"""
def set_section_user_score(request, media_mal_id : int, media_type : str, section_mal_id : int):
    if request.method == "POST":
        score_form = ScoreForm(request.POST)
        if score_form.is_valid():
            media = use_cases.set_section_user_score(media_mal_id, media_type, section_mal_id, score_form)
            return render(request, 'tracking/media_details.html', context = {'media' : media})
    else:
        score_form = ScoreForm()
    return render(request, "tracking/index.html")
"""


def finish_media(request, mal_id: int, media_type: str):
    media = use_cases.finish_media(mal_id, MediaType(media_type))
    return redirect(request.POST.get("next", "tracking:media_details"))
