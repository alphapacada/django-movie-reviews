var offset = 0;
function loadMoreFromAPI(offset) {
  $.ajax({
    url: `/load_more/${offset}`,
    type: "get",
    success: function (response) {
      newdiv = $(response);
      $("#movie-list").append(newdiv);
      newdiv.hide();
    },
    error: function () {},
  });
}

$(document).ready(function () {
  $(".movie-card").hide();
  $(".movie-card").slice(0, 10).show();
  $("#loadMore").on("click", function (e) {
    e.preventDefault();
    $(".movie-card:hidden").slice(0, 10).slideDown();
    if ($(".movie-card:hidden").length == 0) {
      offset += 20;
      loadMoreFromAPI(offset);
    }
    $("html,body").animate(
      {
        scrollTop: $(this).offset().top,
      },
      1500
    );
  });
  $(document).on("click", ".bookmark", function (e) {
    movieCard = $(this).closest(".movie-card");

    mov = {
      url: movieCard.find(".movie-url").attr("href"),
      display_title: movieCard.find(".movie-title").text(),
      img_src: movieCard.find(".movie-img").attr("src"),
    };

    let bookmark = $(this);
    $.ajax({
      type: "POST",
      url: url_add_bookmark,
      data: mov,
      success: function (response) {
        if (response["deleted"]) {
          bookmark.removeClass("bookmarked");
        } else {
          newdiv = $(response);
          $("#add-bookmark").html(newdiv);
          $("#popup").modal("show");
          bookmark.addClass("bookmarked");
        }

      },
      error: function (response) {
        alert("Error");
      },
    });
  });
});
