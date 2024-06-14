$(document).ready(function () {
  $(document).on(
    "click",
    ".pw-dialog-underlay, .pw-dialog-close, .pw-dialog-cancel",
    function () {
      $("#dialog-portal").empty();
    }
  );
});
