from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def redirect_if_authenticated(redirect_url="punkweb_bb:index"):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapper_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)

        return _wrapper_view

    return decorator
