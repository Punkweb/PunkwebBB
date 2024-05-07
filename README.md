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

## Preview

#### Models

![Models](https://github.com/Punkweb/PunkwebBB/blob/main/images/models.png)

#### Index View

![Index](https://github.com/Punkweb/PunkwebBB/blob/main/images/index.png)

#### Thread View

![Thread](https://github.com/Punkweb/PunkwebBB/blob/main/images/thread.png)
