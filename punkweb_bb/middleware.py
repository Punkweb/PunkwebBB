import datetime
from django.core.cache import cache


class ProfileOnlineCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            cache.set(f"profile_online_{request.user.profile.id}", now, 60 * 5)

        response = self.get_response(request)

        return response
