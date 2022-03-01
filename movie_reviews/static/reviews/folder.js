$(".new-folder").on("click", function (e) {
  $(this).hide();
  $(".create-new-folder").toggleClass("d-none");
});
$("#post-folder").on("submit", function (event) {
  event.preventDefault();
  console.log("form submitted!"); // sanity check
  var serializedData = $(this).serialize();
  $.ajax({
    type: "POST",
    url: url_add_folder,
    data: serializedData,
    success: function (response) {
      console.log("SUCCESS");
      $("#post-folder").trigger("reset");
      $("#popup").modal("hide");
    },
    error: function (response) {
      alert("Error");
    },
  });
});
$("#post-folders").on("submit", function (event) {
  event.preventDefault();
  console.log("form submitted!"); // sanity check
  var serializedData = $(this).serialize();
  $.ajax({
    type: "POST",
    url: url_add_to_folders,
    data: serializedData,
    success: function (response) {
      console.log("SUCCESS");
      $("#post-folders").trigger("reset");
      $("#popup").modal("hide");
    },
    error: function (response) {
      alert("Error");
    },
  });
});
