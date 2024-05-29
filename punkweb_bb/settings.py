from django.conf import settings

PUNKWEB_BB = getattr(settings, "PUNKWEB_BB", {})

SITE_NAME = PUNKWEB_BB.get("SITE_NAME", "PUNKWEB")
SITE_TITLE = PUNKWEB_BB.get("SITE_TITLE", "PunkwebBB")
FAVICON = PUNKWEB_BB.get("FAVICON", "punkweb_bb/favicon.ico")
OG_IMAGE = PUNKWEB_BB.get("OG_IMAGE", None)
SHOUTBOX_ENABLED = PUNKWEB_BB.get("SHOUTBOX_ENABLED", True)
DISCORD_WIDGET_ENABLED = PUNKWEB_BB.get("DISCORD_WIDGET_ENABLED", False)
DISCORD_WIDGET_THEME = PUNKWEB_BB.get("DISCORD_WIDGET_THEME", "dark")
DISCORD_SERVER_ID = PUNKWEB_BB.get("DISCORD_SERVER_ID", None)
