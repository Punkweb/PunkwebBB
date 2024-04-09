from punkweb_bb import settings


def punkweb_bb(request):
    return {
        "punkweb_bb": {
            "settings": settings,
        }
    }
