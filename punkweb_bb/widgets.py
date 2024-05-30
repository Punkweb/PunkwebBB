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


class MarkdownEditorWidget(forms.Textarea):
    template_name = "punkweb_bb/widgets/markdown-editor.html"

    def __init__(self, *args, **kwargs):
        super(MarkdownEditorWidget, self).__init__(*args, **kwargs)
        self.attrs["class"] = "markdown-editor"

    class Media:
        css = {
            "all": (
                "/static/punkweb_bb/vendor/tiny-markdown-editor/dist/tiny-mde.min.css",
            )
        }
        js = (
            "/static/punkweb_bb/vendor/jquery-3.7.0.min.js",
            "/static/punkweb_bb/vendor/tiny-markdown-editor/dist/tiny-mde.min.js",
            "/static/punkweb_bb/editor/markdown-editor.js",
        )
