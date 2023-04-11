from rest_framework.throttling import UserRateThrottle,AnonRateThrottle


class WatchlistThrottle(UserRateThrottle):
    scope = 'watch-list'

