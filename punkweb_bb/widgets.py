from django import forms


class BBCodeEditorWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(BBCodeEditorWidget, self).__init__(*args, **kwargs)
        self.attrs["class"] = "bbcode-editor"

    class Media:
        css = {
            "all": (
                "/static/punkweb_bb/vendor/sceditor-3.2.0/minified/themes/square.min.css",
                "/static/punkweb_bb/editor/bbcode-editor.css",
            )
        }
        js = (
            "/static/punkweb_bb/vendor/jquery-3.7.0.min.js",
            "/static/punkweb_bb/vendor/sceditor-3.2.0/minified/jquery.sceditor.bbcode.min.js",
            "/static/punkweb_bb/vendor/sceditor-3.2.0/minified/icons/material.js",
            "/static/punkweb_bb/editor/bbcode-editor-tags.js",
            "/static/punkweb_bb/editor/bbcode-editor.js",
        )
