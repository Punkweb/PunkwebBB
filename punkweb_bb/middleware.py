from django.core.cache import cache
from django.utils import timezone


class ProfileOnlineCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cache.set(
                f"profile_online_{request.user.profile.id}", timezone.now(), 60 * 5
            )

        response = self.get_response(request)

        return response
