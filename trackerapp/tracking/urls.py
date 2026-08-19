from django.urls import path

from . import views

app_name = "tracking"
urlpatterns = [
    path("", views.index, name="index"),
    path("research", views.research, name="research"),
    path(
        "media/<str:media_type>/<int:mal_id>/details",
        views.media_details,
        name="media_details",
    ),
    path(
        "media/<str:media_type>/<int:mal_id>/details/translated",
        views.trasnlate_synopsis,
        name="translated_synopsis",
    ),
    path(
        "media/<str:media_type>/<int:mal_id>/add",
        views.add_media_to_watchlist,
        name="add_to_watchlist",
    ),
    path("finished", views.finished_medias, name="finished_medias"),
    path("watchlists", views.watchlists, name="watchlists"),
    path("watchlist/create", views.create_watchlist, name="watchlist_create"),
    path("watchlist/<str:name>", views.watchlist_details, name="watchlist_details"),
    path(
        "watchlist/<str:name>/remove/<str:media_type>/<int:media_mal_id>",
        views.remove_media_from_watchlist,
        name="remove_to_watchlist",
    ),
    path(
        "watchlist/<str:name>/delete", views.delete_watchlist, name="watchlist_delete"
    ),
    path(
        "media/<str:media_type>/<int:mal_id>/finish/next",
        views.complete_media_next_section,
        name="complete_next",
    ),
    path(
        "media/<str:media_type>/<int:mal_id>/finish/select",
        views.complete_media_section,
        name="set_current_section",
    ),
    path(
        "media/<str:media_type>/<int:mal_id>/finish",
        views.finish_media,
        name="finish_media",
    ),
    path(
        "media/<str:media_type>/<int:mal_id>/score",
        views.set_media_user_score,
        name="set_media_user_score",
    ),
    # path('media/<str:media_type>/<int:media_mal_id>/<int:section_mal_id>/score', views.set_section_user_score, name="set_media_user_score"),
]
