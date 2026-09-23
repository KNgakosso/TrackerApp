from django.urls import path

from . import views

app_name = "tracking"
urlpatterns = [
    path("", views.index, name="index"),
    path("finished", views.finished_medias, name="finished_medias"),
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
