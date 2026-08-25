from django import template
from django.utils.translation import get_language

register = template.Library()
from django.utils.translation import gettext_lazy as _

from ..domain.media import Media
from ..enums import MediaType


@register.simple_tag
def title_translated(media: Media) -> str:
    language_code = get_language()
    if language_code == "fr":
        return media.title_french or media.title_english or media.title
    else:
        return media.title_english or media.title


@register.simple_tag
def section_type(media_type: MediaType):
    if media_type == MediaType.ANIME:
        return _("Episode")
    elif media_type == MediaType.MANGA:
        return _("Volume")
