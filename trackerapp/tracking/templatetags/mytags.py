from django import template
from django.utils.translation import get_language

register = template.Library()
from ..domain.media import Media


@register.simple_tag
def title_translated(media: Media) -> str:
    language_code = get_language()
    if language_code == "fr":
        return media.title_french or media.title_english or media.title
    else:
        return media.title_english or media.title
