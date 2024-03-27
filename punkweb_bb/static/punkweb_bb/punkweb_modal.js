$(document).ready(function () {
  $(document).on(
    "click",
    ".modal__underlay, .modal__close, .modal__cancel",
    function () {
      $(".modal").remove();
    }
  );
});
