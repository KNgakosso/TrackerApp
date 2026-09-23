from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import WatchlistForm, WatchlistSelectionForm


@login_required
def watchlists(request):
    return render(
        request,
        "tracking/watchlists.html",
        context={
            "watchlist_form": WatchlistForm(),
            "watchlists": storage_services.get_watchlists(user=request.user),
        },
    )


@login_required
def create_watchlist(request):
    if request.method == "POST":
        watchlist_form = WatchlistForm(request.POST)
        if watchlist_form.is_valid():
            watchlist = use_cases.create_watchlist(
                watchlist_form=watchlist_form, user=request.user
            )
            return render(
                request,
                "tracking/watchlist_details.html",
                context={"watchlist": watchlist},
            )
    else:
        watchlist_form = WatchlistForm()
    watchlists = storage_services.get_watchlists(user=request.user)
    return render(
        request,
        "tracking/watchlists.html",
        context={"watchlist_form": watchlist_form, "watchlists": watchlists},
    )


@login_required
def watchlist_details(request, name: str):
    watchlist = storage_services.get_watchlist(user=request.user, name=name)
    return render(
        request, "tracking/watchlist_details.html", context={"watchlist": watchlist}
    )


def rename_watchlist(request, name: str):
    if request.method == "POST":
        watchlist_form = WatchlistForm(request.POST)
        if watchlist_form.is_valid():
            watchlist = use_cases.rename_watchlist(
                user=request.user, name=name, watchlist_form=watchlist_form
            )
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
            "watchlists": storage_services.get_watchlists(user=request.user),
            "search_form": SearchForm(),
            "medias": basis.get_ongoing_medias(),
        },
    )


@login_required
def add_media_to_watchlist(request, mal_id: int, media_type: str):
    if request.method == "POST":
        watchlist_selection_form = WatchlistSelectionForm(
            request.POST, user=request.user
        )
        if watchlist_selection_form.is_valid():
            watchlist_name = watchlist_selection_form.cleaned_data["name"]
            watchlist = use_cases.add_media_to_watchlist(
                user=request.user,
                watchlist_name=watchlist_name,
                media_mal_id=mal_id,
                media_type=MediaType(media_type),
            )
            return redirect(
                "tracking:media_details", mal_id=mal_id, media_type=media_type
            )
    else:
        watchlist_selection_form = WatchlistSelectionForm(user=request.user)
    media = basis.get_or_fetch_media(mal_id, MediaType(media_type))
    return render(
        request,
        "tracking/add_to_watchlist.html",
        context={"media": media, "watchlist_selection_form": watchlist_selection_form},
    )


@login_required
def remove_media_from_watchlist(
    request, watchlist_name: str, media_mal_id: int, media_type: str
):
    watchlist = use_cases.remove_media_from_watchlist(
        user=request.user,
        watchlist_name=watchlist_name,
        media_mal_id=media_mal_id,
        media_type=MediaType(media_type),
    )
    return render(
        request, "tracking/watchlist_details.html", context={"watchlist": watchlist}
    )


@login_required
def delete_watchlist(request, name: str):
    storage_services.delete_watchlist(user=request.user, name=name)
    watchlists = storage_services.get_watchlists(user=request.user)
    return redirect("tracking:watchlists")
