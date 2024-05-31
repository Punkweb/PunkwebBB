$(function () {
  $(document).ready(function () {
    $(".bbcode-editor").sceditor({
      emoticonsEnabled: false,
      format: "bbcode",
      icons: "material",
      style: "/static/punkweb_bb/editor/bbcode-editor-content.css",
      toolbar:
        "removeformat,bold,italic,size,color,font,strike,underline|orderedlist,bulletlist|left,center,right|link,image|horizontalrule,quote,code|maximize,source",
      height: "300px",
      width: "100%",
    });
  });
});
