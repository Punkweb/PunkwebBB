# PunkwebBB

PunkwebBB is a Django application that provides a simple and modern forum board software for your Django website.

This is the successor to [punkweb-boards](https://github.com/Punkweb/punkweb-boards).

Check out [punkweb.net](https://punkweb.net/board/) for documentation, support and a live demonstration of the software.

## Built with

- [Django](https://www.djangoproject.com/)
- [django-precise-bbcode](https://github.com/ellmetha/django-precise-bbcode)
- [Markdown](https://python-markdown.github.io/)
- [HTMX](https://htmx.org/)
- [jQuery](https://jquery.com/)
- [SCEditor](https://www.sceditor.com/)
- [TinyMDE](https://github.com/jefago/tiny-markdown-editor)
- [PrismJS](https://prismjs.com/)

## Requirements

- Python 3.9+
- Django 4.0+
- django-precise-bbcode 1.2+
- markdown 3.6+
- Pillow

It may work with older versions of Python and Django, but it has not been tested.

## BBCode or Markdown?

PunkwebBB supports both BBCode and Markdown. You'll want to decide before installing which renderer you want to use, as switching between them will cause existing threads, posts, signatures, etc. to render incorrectly! Switching will not affect the database schema, but it will affect the content.

BBCode is the default renderer, but you can switch to Markdown by setting the following in your Django settings module:

```python
PUNKWEB_BB = {
  "RENDERER": "markdown",
}
```

## Installation

```bash
pip install punkweb-bb
```

Add `precise_bbcode` and `punkweb_bb` to your `INSTALLED_APPS` in your Django settings module:

```python
INSTALLED_APPS = [
    ...
    "precise_bbcode",
    "punkweb_bb",
]
```

_Note_: `precise_bbcode` is required even if using the Markdown renderer! It must be installed before `punkweb_bb`.

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
  "RENDERER": "bbcode", # "bbcode" or "markdown"
  "FAVICON": "punkweb_bb/favicon.ico",
  "OG_IMAGE": None, # Used for Open Graph meta tags, must be a full URL!
  "SHOUTBOX_ENABLED": True,
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
Ran 59 tests in 9.166s

OK
Destroying test database for alias 'default'...
Name                                           Stmts   Miss  Cover
------------------------------------------------------------------
punkweb_bb/__init__.py                             0      0   100%
punkweb_bb/admin.py                               43      0   100%
punkweb_bb/admin_forms.py                         34      0   100%
punkweb_bb/apps.py                                 6      0   100%
punkweb_bb/context_processors.py                   3      0   100%
punkweb_bb/forms.py                               47      0   100%
punkweb_bb/guests.py                              13      0   100%
punkweb_bb/middleware.py                          14      0   100%
punkweb_bb/mixins.py                              11      0   100%
punkweb_bb/models.py                             153      1    99%
punkweb_bb/pagination.py                          11      4    64%
punkweb_bb/parsers.py                             50     36    28%
punkweb_bb/response.py                             3      0   100%
punkweb_bb/settings.py                            11      0   100%
punkweb_bb/signals.py                              9      0   100%
punkweb_bb/templatetags/__init__.py                0      0   100%
punkweb_bb/templatetags/can_delete.py              5      0   100%
punkweb_bb/templatetags/can_edit.py                5      0   100%
punkweb_bb/templatetags/can_post.py                5      0   100%
punkweb_bb/templatetags/humanize_int.py            9      5    44%
punkweb_bb/templatetags/render.py                 36     12    67%
punkweb_bb/templatetags/shoutbox_render.py        18      2    89%
punkweb_bb/templatetags/styled_group_name.py       7      1    86%
punkweb_bb/templatetags/styled_username.py         6      0   100%
punkweb_bb/tests.py                              418      0   100%
punkweb_bb/urls.py                                 4      0   100%
punkweb_bb/utils.py                               42     24    43%
punkweb_bb/views.py                              304    118    61%
punkweb_bb/widgets.py                             16      0   100%
------------------------------------------------------------------
TOTAL                                           1283    203    84%
```
