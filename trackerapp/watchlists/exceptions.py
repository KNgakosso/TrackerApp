class WatchlistError(TrackingError):
    pass


class WatchlistNotFoundError(WatchlistError, NotFoundError):
    pass
