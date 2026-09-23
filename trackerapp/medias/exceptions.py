class TrackingError(Exception):
    pass


class MediaError(TrackingError):
    pass


class NotFoundError(TrackingError):
    pass


class MediaNotFoundError(MediaError, NotFoundError):
    pass


class StorageError(TrackingError):
    pass


class ArgosError(TrackingError):
    pass
