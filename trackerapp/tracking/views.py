from functools import wraps

from django.shortcuts import redirect, render

from .enums import MediaType
from .exceptions import ExternalApiError
from .forms import (
    ScoreForm,
    SearchForm,
    SectionNumberForm,
    WatchlistForm,
    WatchlistSelectionForm,
)
from .services.api.tenrai import tenrai_services
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


def index(request):
    return render(
        request,
        "tracking/index.html",
        context={
            "watchlists": storage_services.get_watchlists(),
            "search_form": SearchForm(),
            "medias": basis.get_ongoing_medias(),
        },
    )


def finished_medias(request):
    medias = basis.get_finished_medias()
    return render(request, "tracking/finished_medias.html", context={"medias": medias})


@handle_api_errors
def research(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_results = tenrai_services.research_media(search_form)
            return render(
                request,
                "tracking/research.html",
                context={"search_results": search_results, "search_form": search_form},
            )
    else:
        search_form = SearchForm()
    return render(request, "tracking/index.html", context={"search_form": search_form})


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


def trasnlate_synopsis(request, mal_id: int, media_type: str):
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


def create_watchlist(request):
    if request.method == "POST":
        watchlist_form = WatchlistForm(request.POST)
        if watchlist_form.is_valid():
            watchlist = use_cases.create_watchlist(watchlist_form)
            return render(
                request,
                "tracking/watchlist_details.html",
                context={"watchlist": watchlist},
            )
    else:
        watchlist_form = WatchlistForm()
    watchlists = storage_services.get_watchlists()
    return render(
        request,
        "tracking/watchlists.html",
        context={"watchlist_form": watchlist_form, "watchlists": watchlists},
    )


def watchlist_details(request, name: str):
    watchlist = storage_services.get_watchlist(name=name)
    return render(
        request, "tracking/watchlist_details.html", context={"watchlist": watchlist}
    )


def add_media_to_watchlist(request, mal_id: int, media_type: str):
    if request.method == "POST":
        watchlist_selection_form = WatchlistSelectionForm(request.POST)
        if watchlist_selection_form.is_valid():
            watchlist_name = watchlist_selection_form.cleaned_data["name"]
            watchlist = use_cases.add_media_to_watchlist(
                watchlist_name, mal_id, MediaType(media_type)
            )
            return redirect(
                "tracking:media_details", mal_id=mal_id, media_type=media_type
            )
    else:
        watchlist_selection_form = WatchlistSelectionForm()
    media = basis.get_or_fetch_media(mal_id, MediaType(media_type))
    return render(
        request,
        "tracking/add_to_watchlist.html",
        context={"media": media, "watchlist_selection_form": watchlist_selection_form},
    )


def remove_media_from_watchlist(
    request, watchlist_name: str, media_mal_id: int, media_type: str
):
    watchlist = use_cases.remove_media_from_watchlist(
        watchlist_name, media_mal_id, MediaType(media_type)
    )
    return render(
        request, "tracking/watchlist_details.html", context={"watchlist": watchlist}
    )


def delete_watchlist(request, name: str):
    storage_services.delete_watchlist(name)
    watchlists = storage_services.get_watchlists()
    return redirect("tracking:watchlists")


def complete_media_next_section(request, mal_id: int, media_type: str):
    media = use_cases.complete_media_next_section(mal_id, MediaType(media_type))
    return render(
        request,
        "tracking/media_details.html",
        context={
            "media": media,
            "watchlist_selection_form": WatchlistSelectionForm(),
            "section_number_form": basis.get_section_number_form(media),
            "score_form": ScoreForm(),
        },
    )


def complete_media_section(request, mal_id: int, media_type: str):
    if request.method == "POST":
        section_number_form = SectionNumberForm(request.POST, max_value=100)
        if section_number_form.is_valid():
            media = use_cases.set_media_current_user_section(
                mal_id, MediaType(media_type), section_number_form
            )
            return render(
                request,
                "tracking/media_details.html",
                context={
                    "media": media,
                    "watchlist_selection_form": WatchlistSelectionForm(),
                    "section_number_form": basis.get_section_number_form(media),
                    "score_form": ScoreForm(),
                },
            )

    return redirect("tracking:media_details", mal_id=mal_id, media_type=media_type)


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
                    "watchlist_selection_form": WatchlistSelectionForm(),
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
            "watchlists": storage_services.get_watchlists(),
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
    return render(
        request,
        "tracking/index.html",
        context={
            "watchlists": storage_services.get_watchlists(),
            "search_form": SearchForm(),
            "medias": basis.get_ongoing_medias(),
        },
    )


def rename_watchlist(request, name: str):
    if request.method == "POST":
        watchlist_form = WatchlistForm(request.POST)
        if watchlist_form.is_valid():
            watchlist = use_cases.rename_watchlist(name, watchlist_form)
            return render(
                request,
                "tracking/watchlist_details.html",
                context={"watchlist": watchlist},
            )
    else:
        watchlist_form = WatchlistForm()
    return render(
        request,
        "tracking/index.html",
        context={
            "watchlists": storage_services.get_watchlists(),
            "search_form": SearchForm(),
            "medias": basis.get_ongoing_medias(),
        },
    )


def watchlists(request):
    return render(
        request,
        "tracking/watchlists.html",
        context={
            "watchlist_form": WatchlistForm(),
            "watchlists": storage_services.get_watchlists(),
        },
    )
