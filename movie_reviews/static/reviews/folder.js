$(document).ready(function() {
  $(document).on('click', '.new-folder', function (e) {
  $(this).hide();
  $(".create-new-folder").toggleClass("d-none");
});
$(document).on('submit', "#post-folder", function(event) {
  event.preventDefault();
  var serializedData = $(this).serialize();
  var url_add_folder = $(this).attr('action');
  $.ajax({
    type: "POST",
    url: url_add_folder,
    data: serializedData,
    success: function (response) {
      $("#post-folder").trigger("reset");
      $("#popup").modal("hide");
    },
    error: function (response) {
      alert("Error");
    },
  });
});
$(document).on("submit", "#post-folders", function (event) {
  event.preventDefault();
  var serializedData = $(this).serialize();
  var url_add_to_folders = $(this).attr('action')
  $.ajax({
    type: "POST",
    url: url_add_to_folders,
    data: serializedData,
    success: function (response) {
      $("#post-folders").trigger("reset");
      $("#popup").modal("hide");
    },
    error: function (response) {
      alert("Error");
    },
  });
});
});
