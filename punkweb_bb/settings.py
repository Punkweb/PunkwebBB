from django.conf import settings

PUNKWEB_BB = getattr(settings, "PUNKWEB_BB", {})

SITE_NAME = PUNKWEB_BB.get("SITE_NAME", "PUNKWEB")
SITE_TITLE = PUNKWEB_BB.get("SITE_TITLE", "PunkwebBB")
FAVICON = PUNKWEB_BB.get("FAVICON", "punkweb_bb/favicon.ico")
SHOUTBOX_ENABLED = PUNKWEB_BB.get("SHOUTBOX_ENABLED", True)
