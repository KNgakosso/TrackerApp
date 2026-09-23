from django import forms
from django.utils.translation import gettext_lazy as _


class ScoreForm(forms.Form):
    score = forms.IntegerField(min_value=0, max_value=10)


class SectionNumberForm(forms.Form):
    section_number = forms.TypedChoiceField(coerce=int, label=_("Section number"))

    def __init__(self, *args, max_value: int = 0, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["section_number"].choices = [(0, "--")] + [
            (i, str(i)) for i in range(1, max_value + 1)
        ]
