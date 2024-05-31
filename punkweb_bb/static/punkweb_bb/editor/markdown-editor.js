function initMarkdownEditor(containerElement) {
  var editorElement = containerElement.querySelector(".markdown-editor");
  var toolbarElement = containerElement.querySelector(
    "#markdown-editor-toolbar"
  );

  var editor = null;

  if (!containerElement.querySelector(".TinyMDE")) {
    editor = new TinyMDE.Editor({
      textarea: editorElement,
    });
  }

  if (editor && !toolbarElement.querySelector(".TMCommandBar")) {
    var toolbar = new TinyMDE.CommandBar({
      element: toolbarElement,
      editor: editor,
      commands: [
        "bold",
        "italic",
        "strikethrough",
        "|",
        "h1",
        "h2",
        "|",
        "ul",
        "ol",
        "|",
        "blockquote",
        "code",
        "insertLink",
        "insertImage",
        "hr",
      ],
    });
  }
}

$(function () {
  $(document).ready(function () {
    var editorElements = document.querySelectorAll(
      ".markdown-editor-container"
    );
    editorElements.forEach((element) => {
      initMarkdownEditor(element);
    });
  });
});
