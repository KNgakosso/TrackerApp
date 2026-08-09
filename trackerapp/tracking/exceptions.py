class TrackingError(Exception):
    pass


class MediaError(TrackingError):
    pass


class WatchlistError(TrackingError):
    pass


class NotFoundError(TrackingError):
    pass


class MediaNotFoundError(MediaError, NotFoundError):
    pass


class WatchlistNotFoundError(WatchlistError, NotFoundError):
    pass


class StorageError(TrackingError):
    pass


class InvalidScoreError(MediaError):
    pass


class ExternalApiError(TrackingError):
    pass
