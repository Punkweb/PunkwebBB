from django.core.cache import cache
from django.utils import timezone

from punkweb_bb.guests import guest_list


class ProfileOnlineCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cache.set(
                f"profile_online_{request.user.profile.id}", timezone.now(), 60 * 5
            )
        else:
            ip = request.META.get("REMOTE_ADDR")
            guest_list.add(ip)

        guest_list.clear_expired()

        response = self.get_response(request)

        return response
