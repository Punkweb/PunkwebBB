$(function () {
  $(document).ready(function () {
    sceditor.formats.bbcode.set("code", {
      tags: {
        code: null,
      },
      isInline: false,
      isHtmlInline: false,
      allowedChildren: ["#"],
      skipLastLineBreak: true,
      format: function (element, content) {
        var languageClass = element.classList[0];

        if (languageClass) {
          var language = languageClass.split("-")[1];
          return "[code=" + language + "]" + content + "[/code]";
        }

        return "[code]" + content + "[/code]";
      },
      html: function (token, attrs, content) {
        var language = attrs.defaultattr;

        if (language) {
          return (
            "<pre><code class='language-" +
            language +
            "'>" +
            content +
            "</code></pre>"
          );
        }

        return "<pre><code>" + content + "</code></pre>";
      },
    });
    sceditor.formats.bbcode.set("shadow", {
      tags: {
        span: {
          id: "bbcode-shadow",
        },
      },
      quoteType: 2,
      format: function (element, content) {
        var textShadow = element.style.textShadow;
        if (!textShadow) {
          return content;
        }
        var shadowColor = textShadow.split(" 0px")[0];
        return "[shadow=" + shadowColor + "]" + content + "[/shadow]";
      },
      html: function (token, attrs, content) {
        return (
          '<span id="bbcode-shadow" style="text-shadow: 0px 0px 1em ' +
          attrs.defaultattr +
          '">' +
          content +
          "</span>"
        );
      },
    });
  });
});
