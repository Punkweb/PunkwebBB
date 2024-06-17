# PunkwebBB

PunkwebBB is a Django application that provides a simple and modern forum board software for your Django website.

Check out [punkweb.net](https://punkweb.net/board/) for documentation, support and a live demonstration of the software.

## Built with

- [Django](https://www.djangoproject.com/)
- [HTMX](https://htmx.org/)
- [jQuery](https://jquery.com/)
- [bbcode](https://pypi.org/project/bbcode/)
- [Markdown](https://pypi.org/project/Markdown/)
- [SCEditor](https://www.sceditor.com/)
- [TinyMDE](https://github.com/jefago/tiny-markdown-editor)
- [PrismJS](https://prismjs.com/)

## Requirements

- Python 3.9+
- Django 4.0+

It may work with older versions of Python and Django, but it has not been tested.

## Installation

```bash
pip install punkweb-bb
```

Add `punkweb_bb` to your `INSTALLED_APPS` in your Django settings module:

```python
INSTALLED_APPS = [
    ...
    "punkweb_bb",
]
```

Add the following context processor to your `TEMPLATES` setting:

```python
TEMPLATES = [
    {
        ...
        "OPTIONS": {
            "context_processors": [
                ...
                "punkweb_bb.context_processors.punkweb_bb",
            ],
        },
    },
]
```

**_Note_**: The context processor is deprecated and will be removed in v0.5.0!

Add the following URL pattern to your `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path("forum/", include("punkweb_bb.urls")), # or any other path you want
]
```

And finally, install the models:

```bash
python manage.py migrate
```

## Configuration

These are the default settings for PunkwebBB, which can be overridden in your Django settings module:

```python
PUNKWEB_BB = {
  "SITE_NAME": "PUNKWEB",
  "SITE_TITLE": "PunkwebBB",
  "PARSER": "bbcode", # "bbcode" or "markdown"
  "FAVICON": "punkweb_bb/favicon.ico",
  "OG_IMAGE": None, # Used for Open Graph meta tags, must be a full URL!
  "SHOUTBOX_ENABLED": True,
  "SHOUTBOX_POLLING_ENABLED": True,
  "SHOUTBOX_POLLING_INTERVAL": 30, # in seconds
  "DISCORD_WIDGET_ENABLED": False,
  "DISCORD_WIDGET_THEME": "dark",
  "DISCORD_SERVER_ID": None, # Found under Server Settings > Widget > Server ID
}
```

## Testing

Report:

```bash
coverage run && coverage report
```

HTML:

```bash
coverage run && coverage html
```

```bash
Found 59 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...........................................................
----------------------------------------------------------------------
Ran 59 tests in 8.389s

OK
Destroying test database for alias 'default'...
Name                                           Stmts   Miss  Cover
------------------------------------------------------------------
punkweb_bb/__init__.py                             0      0   100%
punkweb_bb/admin.py                               42      0   100%
punkweb_bb/admin_forms.py                         34      0   100%
punkweb_bb/apps.py                                 6      0   100%
punkweb_bb/bbcode.py                             118     46    61%
punkweb_bb/decorators.py                          12      0   100%
punkweb_bb/forms.py                               59      0   100%
punkweb_bb/guests.py                              13      0   100%
punkweb_bb/middleware.py                          14      0   100%
punkweb_bb/mixins.py                              11      0   100%
punkweb_bb/models.py                             154      1    99%
punkweb_bb/pagination.py                          11      4    64%
punkweb_bb/response.py                             3      0   100%
punkweb_bb/searching.py                            8      5    38%
punkweb_bb/settings.py                            13      0   100%
punkweb_bb/signals.py                              9      0   100%
punkweb_bb/templatetags/__init__.py                0      0   100%
punkweb_bb/templatetags/can_delete.py              5      0   100%
punkweb_bb/templatetags/can_edit.py                5      0   100%
punkweb_bb/templatetags/can_post.py                5      0   100%
punkweb_bb/templatetags/humanize_int.py            9      5    44%
punkweb_bb/templatetags/punkweb_bb.py              6      0   100%
punkweb_bb/templatetags/render.py                 38     16    58%
punkweb_bb/templatetags/styled_group_name.py       7      1    86%
punkweb_bb/templatetags/styled_username.py         6      0   100%
punkweb_bb/tests.py                              418      0   100%
punkweb_bb/urls.py                                 4      0   100%
punkweb_bb/utils.py                               44     26    41%
punkweb_bb/views.py                              319    123    61%
punkweb_bb/widgets.py                             16      2    88%
------------------------------------------------------------------
TOTAL                                           1389    229    84%
```
