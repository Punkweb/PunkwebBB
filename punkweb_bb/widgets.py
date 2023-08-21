from django import forms


class BBCodeEditor(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(BBCodeEditor, self).__init__(*args, **kwargs)
        self.attrs["class"] = "bbcode-editor"

    class Media:
        css = {
            "all": (
                "/static/punkweb_bb/sceditor-3.2.0/minified/themes/square.min.css",
                "/static/punkweb_bb/bbcode-editor.css",
            )
        }
        js = (
            "/static/punkweb_bb/jquery-3.7.0.min.js",
            "/static/punkweb_bb/sceditor-3.2.0/minified/jquery.sceditor.bbcode.min.js",
            "/static/punkweb_bb/sceditor-3.2.0/minified/icons/material.js",
            "/static/punkweb_bb/bbcode-editor.js",
        )
