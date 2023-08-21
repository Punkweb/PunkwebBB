$(function () {
  $(document).ready(function () {
    $(".bbcode-editor").sceditor({
      emoticonsCompat: true,
      emoticonsEnabled: false,
      emoticonsRoot: "/media/precise_bbcode/smilies/",
      fonts:
        "Arial,Arial Black,Comic Sans MS,Inconsolata,Courier New,Georgia,Impact,Open Sans,Montserrat,Sans-serif,Serif,Times New Roman,Trebuchet MS,Verdana",
      format: "bbcode",
      icons: "material",
      style: "/static/punkweb_bb/bbcode-editor-content.css",
      toolbar:
        "bold,italic,underline,strike|bulletlist,orderedlist,center,horizontalrule|font,size,color,quote,code,link,image|date,time|source,maximize,removeformat",
    });
  });
});
