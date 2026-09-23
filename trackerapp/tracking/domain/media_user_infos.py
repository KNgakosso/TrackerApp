from dataclasses import dataclass

from ..enums import MediaCompletion


@dataclass
class MediaUserInfos:
    score: int | None
    completion: MediaCompletion
    current_section: int | None
