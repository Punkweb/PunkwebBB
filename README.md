# PunkwebBB

PunkwebBB is a Django application that provides a simple and modern forum board software for your Django website.

This is the successor to [punkweb-boards](https://github.com/Punkweb/punkweb-boards).

Check out [punkweb.net](https://punkweb.net/board/) for a live demo and more information!

## Built with

- [Django](https://www.djangoproject.com/)
- [django-precise-bbcode](https://github.com/ellmetha/django-precise-bbcode)
- [HTMX](https://htmx.org/)
- [jQuery](https://jquery.com/)
- [SCEditor](https://www.sceditor.com/)
- [PrismJS](https://prismjs.com/)

## Requirements

- Python 3.11+
- Django 4.2+
- django-precise-bbcode 1.2+
- Pillow

It may work with older versions of Python and Django, but it has not been tested.

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

_Note_: `precise_bbcode` is required. It must be installed before `punkweb_bb`.

Add the following middleware to your `MIDDLEWARE` setting:

```python
MIDDLEWARE = [
    ...
    "punkweb_bb.middleware.ProfileOnlineCacheMiddleware",
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
  "FAVICON": "punkweb_bb/favicon.ico",
  "SHOUTBOX_ENABLED": True,
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
Found 57 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........................................................
----------------------------------------------------------------------
Ran 57 tests in 8.824s

OK
Destroying test database for alias 'default'...
Name                                         Stmts   Miss  Cover
----------------------------------------------------------------
punkweb_bb/__init__.py                           0      0   100%
punkweb_bb/admin.py                             41      1    98%
punkweb_bb/admin_forms.py                       28      0   100%
punkweb_bb/apps.py                               6      0   100%
punkweb_bb/bbcode_tags.py                      115      3    97%
punkweb_bb/context_processors.py                 3      0   100%
punkweb_bb/forms.py                             35      0   100%
punkweb_bb/middleware.py                        10      0   100%
punkweb_bb/mixins.py                            11      0   100%
punkweb_bb/models.py                           124      0   100%
punkweb_bb/pagination.py                        11      4    64%
punkweb_bb/parsers.py                           50      2    96%
punkweb_bb/response.py                           3      0   100%
punkweb_bb/settings.py                           6      0   100%
punkweb_bb/signals.py                            9      0   100%
punkweb_bb/templatetags/__init__.py              0      0   100%
punkweb_bb/templatetags/humanize_int.py          9      5    44%
punkweb_bb/templatetags/shoutbox_bbcode.py       9      0   100%
punkweb_bb/tests.py                            410      0   100%
punkweb_bb/urls.py                               4      0   100%
punkweb_bb/views.py                            174     17    90%
punkweb_bb/widgets.py                            8      0   100%
----------------------------------------------------------------
TOTAL                                         1066     32    97%
```
