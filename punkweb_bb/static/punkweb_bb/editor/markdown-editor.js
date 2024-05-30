function initMarkdownEditor(element) {
  var editor = new TinyMDE.Editor({
    textarea: element,
  });

  var toolbarElement = document.createElement("div");
  toolbarElement.id = "markdown-editor-toolbar";
  element.parentNode.insertBefore(toolbarElement, element);

  new TinyMDE.CommandBar({
    element: toolbarElement,
    editor: editor,
  });
}

$(function () {
  $(document).ready(function () {
    var editorElements = document.querySelectorAll(".markdown-editor");
    editorElements.forEach((element) => {
      initMarkdownEditor(element);
    });
  });
});
