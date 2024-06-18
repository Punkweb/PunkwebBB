from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
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
            ip = self.get_client_ip(request)
            guest_list.add(ip)

        guest_list.clear_expired()

        response = self.get_response(request)

        return response

    def get_client_ip(self, request):
        headers = (
            "HTTP_X_FORWARDED_FOR",
            "HTTP_X_REAL_IP",
            "HTTP_CLIENT_IP",
            "HTTP_X_CLIENT_IP",
            "HTTP_X_CLUSTER_CLIENT_IP",
            "HTTP_FORWARDED_FOR",
            "HTTP_FORWARDED",
            "REMOTE_ADDR",
        )

        for header in headers:
            ip = request.META.get(header, None)
            if ip:
                try:
                    validate_ipv46_address(ip)
                    return ip
                except ValidationError:
                    pass

        return ""
