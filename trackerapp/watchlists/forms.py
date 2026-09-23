from typing import ClassVar

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import WatchlistModel


class WatchlistForm(forms.ModelForm):
    class Meta:
        model = WatchlistModel
        fields: ClassVar = ["name"]
        labels: ClassVar = {"name": _("Name")}


class WatchlistSelectionForm(forms.Form):
    name = forms.ModelChoiceField(
        label=_("Name"),
        queryset=WatchlistModel.objects.none(),
        empty_label=_("-- Choose a list --"),
    )

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].queryset = WatchlistModel.objects.filter(user=user)
