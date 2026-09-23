from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from medias.enums import AnimeRating
from medias.models.media_models import DemographicModel, GenreModel, ThemeModel


class SearchForm(forms.Form):
    q = forms.CharField(label=_("Title"), required=False)

    rating = forms.ChoiceField(
        label=_("Rating"),
        choices=[
            ("", "--"),
            *[(rating.filter_value, rating.display) for rating in AnimeRating],
        ],
        required=False,
    )
    min_score = forms.FloatField(
        label=_("Min score"), min_value=0, max_value=10, required=False
    )
    max_score = forms.FloatField(
        label=_("Max score"), min_value=0, max_value=10, required=False
    )
    if settings.SFW:
        sfw = forms.BooleanField(
            initial=True,
            label=_("SFW"),
            required=False,
            disabled=True,
            widget=forms.HiddenInput(),
        )
    else:
        sfw = forms.BooleanField(initial=True, label=_("SFW"), required=False)

    genres = forms.ModelMultipleChoiceField(
        queryset=GenreModel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    excluded_themes = ["Erotica", "Hentai"] if settings.SFW else []
    themes = forms.ModelMultipleChoiceField(
        queryset=ThemeModel.objects.exclude(name__in=excluded_themes),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    demographics = forms.ModelMultipleChoiceField(
        queryset=DemographicModel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    type = forms.MultipleChoiceField(
        choices=[("manga", "manga"), ("anime", "anime")],
        required=True,
        widget=forms.CheckboxSelectMultiple(),
        initial=["anime", "manga"],
    )

    def clean_rating(self):
        rating = self.cleaned_data.get("rating") or None
        return rating

    def clean(self):
        min_score = self.cleaned_data.get("min_score")
        max_score = self.cleaned_data.get("max_score")
        if min_score is not None and max_score is not None:
            if min_score > max_score:
                raise forms.ValidationError(
                    "Le score minimal ne peut pas être plus grand que le score maximal."
                )
        return min_score
