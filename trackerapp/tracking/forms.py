from django import forms
from django.utils.translation import gettext_lazy as _

from .enums import AnimeRating
from .models.media_models import DemographicModel, GenreModel, ThemeModel
from .models.watchlist_model import WatchlistModel


class WatchlistForm(forms.ModelForm):
    class Meta:
        model = WatchlistModel
        fields = ["name"]
        labels = {"name": _("Name")}


class ScoreForm(forms.Form):
    score = forms.IntegerField(min_value=0, max_value=10)


class SectionNumberForm(forms.Form):
    section_number = forms.TypedChoiceField(coerce=int, label=_("Section number"))

    def __init__(self, *args, max_value: int = 0, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["section_number"].choices = [(0, "--")] + [
            (i, str(i)) for i in range(1, max_value + 1)
        ]


class WatchlistSelectionForm(forms.Form):
    name = forms.ModelChoiceField(
        label=_("Name"),
        queryset=WatchlistModel.objects.all(),
        empty_label=_("-- Choose a list --"),
    )


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
    sfw = forms.BooleanField(initial=True, label=_("SFW"), required=False)
    genres = forms.ModelMultipleChoiceField(
        queryset=GenreModel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    themes = forms.ModelMultipleChoiceField(
        queryset=ThemeModel.objects.all(),
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
