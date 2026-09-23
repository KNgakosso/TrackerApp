from enum import StrEnum

from django.utils.translation import gettext_lazy as _


class MediaCompletion(StrEnum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

    @property
    def display(self):
        return {
            MediaCompletion.NOT_STARTED: _("Not started"),
            MediaCompletion.IN_PROGRESS: _("In progress"),
            MediaCompletion.COMPLETED: _("Completed"),
        }[self]
