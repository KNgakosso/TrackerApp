from django.urls import path

from . import views

app_name = "medias"
urlpatterns = [
    path(
        "media/<str:media_type>/<int:mal_id>/details",
        views.media_details,
        name="media_details",
    ),
    path(
        "media/<str:media_type>/<int:mal_id>/details/translated",
        views.translate_synopsis,
        name="translate_synopsis",
    ),
]
