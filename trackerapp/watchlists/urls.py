from django.urls import path

from . import views

app_name = "watchlists"
urlpatterns = [
    path(
        "media/<str:media_type>/<int:mal_id>/add",
        views.add_media_to_watchlist,
        name="add_to_watchlist",
    ),
    path("watchlists", views.watchlists, name="watchlists"),
    path("watchlist/create", views.create_watchlist, name="watchlist_create"),
    path("watchlist/<str:name>", views.watchlist_details, name="watchlist_details"),
    path(
        "watchlist/<str:watchlist_name>/remove/<str:media_type>/<int:media_mal_id>",
        views.remove_media_from_watchlist,
        name="remove_from_watchlist",
    ),
    path(
        "watchlist/<str:name>/delete", views.delete_watchlist, name="watchlist_delete"
    ),
]
