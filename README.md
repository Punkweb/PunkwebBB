# PunkwebBB

## What is PunkwebBB?

PunkwebBB is a Django application that provides a complete forum board solution for Django websites. What sets it apart is its focus on simplicity and independence - it doesn't rely on other Django apps, making it incredibly straightforward to install and configure. The goal? To have a fully functional forum up and running in under a minute.

Check out [punkweb.net](https://punkweb.net/board/) for documentation, support and a live demonstration of the software.

## Requirements

- Python 3.9+
- Django 3.2+

It may work with older versions of Python and Django, but it has not been tested.

## Key Features

### 1. Modern Technology Stack

- [Django](https://www.djangoproject.com/)
- [HTMX](https://htmx.org/)
- [bbcode](https://pypi.org/project/bbcode/)
- [Markdown](https://pypi.org/project/Markdown/)
- [SCEditor](https://www.sceditor.com/)
- [TinyMDE](https://github.com/jefago/tiny-markdown-editor)
- [PrismJS](https://prismjs.com/)

### 2. Core Functionality

- User registration and authentication
- Thread and post management
- Real-time shoutbox
- Discord integration
- BBCode and Markdown parsing
- Responsive design
- Admin controls and moderation tools

## Getting Started

### Installation

```bash
pip install punkweb-bb
```

### Configuration

Add to your Django settings:

```python
INSTALLED_APPS = [
    ...
    "punkweb_bb",
]
```

**_Optionally:_** Add the following middleware to your `MIDDLEWARE` setting, at the end of the list:

```python
MIDDLEWARE = [
    ...
    "punkweb_bb.middleware.ProfileOnlineCacheMiddleware",
]
```

### URL Configuration

```python
from django.urls import path, include

urlpatterns = [
    ...
    path("forum/", include("punkweb_bb.urls")),
]
```

## Customization Options

PunkwebBB comes with a range of configurable settings:

```python
PUNKWEB_BB = {
    "SITE_NAME": "Your Site Name",
    "SITE_TITLE": "Your Forum Title",
    "PARSER": "bbcode",  # or "markdown"
    "FAVICON": "path/to/favicon.ico",
    "OG_IMAGE": None,  # Full URL for Open Graph meta tags
    "SHOUTBOX_ENABLED": True,
    "SHOUTBOX_POLLING_ENABLED": True,
    "SHOUTBOX_POLLING_INTERVAL": 30,  # seconds
    "DISCORD_WIDGET_ENABLED": False,
    "DISCORD_WIDGET_THEME": "dark",
    "DISCORD_SERVER_ID": None,
}
```

## Why Choose PunkwebBB?

### 1. Simplicity

The installation process is straightforward, and the default configuration works out of the box. You don't need to be a Django expert to get started.

### 2. Independence

Unlike many forum solutions that require multiple dependencies, PunkwebBB is self-contained. This means fewer potential points of failure and easier maintenance.

### 3. Modern Features

From real-time shoutbox to Discord integration, PunkwebBB includes features that modern communities expect.

### 4. Extensibility

While it's simple to set up, PunkwebBB is also highly customizable. You can extend its functionality to match your specific needs.

### 5. Performance

Built with efficiency in mind, PunkwebBB handles user interactions smoothly without unnecessary overhead.

## Real-World Applications

PunkwebBB is ideal for:

- Gaming communities
- Business support forums
- Educational platforms
- Technical discussion boards
- Fan communities
- Knowledge-sharing platforms

## Conclusion

PunkwebBB represents a perfect balance between simplicity and functionality. Whether you're building a small community forum or a large-scale discussion platform, it provides all the essential features while remaining easy to implement and maintain.

The project's focus on independence and straightforward installation makes it an excellent choice for developers who want to add forum functionality to their Django projects without the complexity of larger forum solutions.

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
Ran 59 tests in 8.594s

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
punkweb_bb/middleware.py                          27      3    89%
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
TOTAL                                           1402    232    83%
```
