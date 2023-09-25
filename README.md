# PunkwebBB

Oldschool forum board software written in Django.

This is the successor to [punkweb-boards](https://github.com/Punkweb/punkweb-boards)

## Data Fixtures

As a convience for populating dummy data in development, a fixture file is included that will import 100 users, 4 categories, 11 subcategories, 385 threads, and 2227 posts. You don't have to use it, but it's there.

To load the data, run this command:

```bash
./manage.py loaddata fixtures/initial_data.json
```

## Coverage

Report:

```bash
coverage run && coverage report
```

HTML:

```bash
coverage run && coverage html
```

```
Name                        Stmts   Miss  Cover
-----------------------------------------------
punkweb_bb/__init__.py          0      0   100%
punkweb_bb/admin.py            41      1    98%
punkweb_bb/admin_forms.py      28      0   100%
punkweb_bb/apps.py              6      0   100%
punkweb_bb/bbcode_tags.py      65      3    95%
punkweb_bb/forms.py            22      0   100%
punkweb_bb/mixins.py           11      0   100%
punkweb_bb/models.py           80      0   100%
punkweb_bb/response.py          3      1    67%
punkweb_bb/signals.py           9      0   100%
punkweb_bb/tests.py            85      0   100%
punkweb_bb/urls.py              4      0   100%
punkweb_bb/views.py           124     93    25%
punkweb_bb/widgets.py           8      0   100%
-----------------------------------------------
TOTAL                         486     98    80%
```
