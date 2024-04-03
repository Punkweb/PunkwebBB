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
      format: "bbcode",
      icons: "material",
      style: "/static/punkweb_bb/editor/bbcode-editor-content.css",
      toolbar:
        "removeformat,bold,italic,size,color,font,strike,underline|orderedlist,bulletlist|left,center,right|link,image,emoticon|horizontalrule,quote,code|maximize,source",
      height: "300px",
      width: "100%",
    });
  });
});
