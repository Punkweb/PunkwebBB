$(function () {
  $(document).ready(function () {
    $(".bbcode-editor").sceditor({
      format: "bbcode",
      icons: "material",
      style: "/static/punkweb_bb/bbcode-editor-content.css",
      toolbar:
        "bold,italic,underline,strike|bulletlist,orderedlist,center,horizontalrule|font,size,color,quote,code,link,image|date,time|source,maximize,removeformat",
    });
  });
});
