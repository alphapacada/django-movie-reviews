
var offset = 0;
function loadMoreFromAPI(offset) {
  $.ajax({
    url: `/load_more/${offset}`,
    type: "get",
    success: function (response) {
      console.log(response);
      newdiv = $(response)
      $("#movie-list").append(newdiv);

      // var movies = response.data;
      newdiv.hide();
    },
    error: function () {
      alert("ERROR");
    },
  });
}


$(document).ready(function () {
  // $('[data-bs-toggle="tooltip"]').tooltip();   
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
  $(document).on('click','.bookmark', function(e) {
    movieCard = $(this).closest(".movie-card")
    console.log(movieCard);
    console.log(movieCard.find('.movie-url').attr('href'))
    console.log(movieCard.find('.movie-title').text())
    console.log(movieCard.find('.movie-img').attr('src'))
    
    mov = {
      url: movieCard.find('.movie-url').attr('href'),
      display_title: movieCard.find('.movie-title').text(),
      img_src: movieCard.find('.movie-img').attr('src')
    }
    let bookmark = $(this)
    console.log(mov)
    $.ajax({
      type: 'POST',
      url: url_add_bookmark,
      data: mov,
      success: function (response) {
        bookmark.toggleClass('bookmarked');
        $('#popup').modal('show')


      },
      error: function (response) {
        alert("Error")
      }
    })
  })
})