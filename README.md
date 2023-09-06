# PunkwebBB

Oldschool forum board software written in Django.

This is the successor to [punkweb-boards](https://github.com/Punkweb/punkweb-boards)


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
punkweb_bb/forms.py            17      0   100%
punkweb_bb/mixins.py           11      0   100%
punkweb_bb/models.py           73      0   100%
punkweb_bb/signals.py           9      0   100%
punkweb_bb/tests.py            78      0   100%
punkweb_bb/urls.py              4      0   100%
punkweb_bb/views.py            90     70    22%
punkweb_bb/widgets.py           8      0   100%
-----------------------------------------------
TOTAL                         430     74    83%
```