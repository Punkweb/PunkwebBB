$(function () {
  $(document).ready(function () {
    $(".bbcode-editor").sceditor({
      emoticonsCompat: true,
      emoticonsEnabled: true,
      emoticonsRoot: "/media/precise_bbcode/smilies/",
      emoticons: {
        dropdown: {
          ":smile:": "smile.png",
          ":cool:": "cool.png",
        },
      },
      fonts:
        "Arial,Arial Black,Comic Sans MS,Courier New,Georgia,Impact,Sans-serif,Serif,Times New Roman,Trebuchet MS,Verdana",
      format: "bbcode",
      icons: "material",
      style: "/static/punkweb_bb/bbcode-editor-content.css",
      toolbar:
        "bold,italic,underline,strike|bulletlist,orderedlist,center,horizontalrule|font,size,color,quote,code,emoticon,link,image|date,time|source,maximize,removeformat",
      height: "300px",
      width: "100%",
    });
  });
});
