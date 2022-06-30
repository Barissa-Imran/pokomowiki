$(document).ready(() => {
  // close approve message on x click
  $(".close-btn").on("click", function () {
    $("#approveMessage").slideUp("slow", function () {
      $("#approveMessage").toggleClass("d-none");
      $("#approveMessage p").empty();
    });
  });
  
  // example translate functionality
  $(".exampletrans").on("click", function () {
    var termId = $(this).attr("data-termId");
    // show example translation
    var element = $(".example" + termId);
    if (element.hasClass("d-none")) {
      $(".example" + termId).fadeIn("slow", () => {
        $(".example" + termId).toggleClass("d-none");
      });
    } else {
      $(".example" + termId).fadeOut("slow", () => {
        $(".example" + termId).toggleClass("d-none");
      });
    }

    $(".exampletrans" + termId).fadeIn("slow", () => {
      $(".exampletrans" + termId).toggleClass("d-none");
    });
  });

  // submit approval on button click
  $(".approve").on("click", function (e) {
    e.preventDefault();

    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    let termId = $(this).attr("data-termId");
    $.ajax({
      url: "",
      type: "post",
      data: {
        type: "approve",
        csrfmiddlewaretoken: csrf,
        termId: termId,
      },
      success: function (response) {
        var data = JSON.parse(response["data"]);

        // hide approved term
        $("#accordion" + termId).fadeOut("slow", function () {
          $("#accordion" + termId).hide();
        });
        $("#approveMessage").toggleClass("alert-success");
        $("#approveMessage").toggleClass("d-none");
        $("#approveMessage p").prepend(data["message"]);

        $("#approveMessage").slideDown("slow", function () {
          $("#approveMessage")
            .delay(3000)
            .slideUp("slow", function () {
              $("#approveMessage").toggleClass("alert-success");
              $("#approveMessage").toggleClass("d-none");
              $("#approveMessage p").empty();
            });
        });
      },
      error: function (response) {
        var data = JSON.parse(response.responseJSON["data"]);

        $("#approveMessage").toggleClass("d-none");
        $("#approveMessage").toggleClass("alert-danger");
        $("#approveMessage p").prepend(data["message"]);

        $("#approveMessage").slideDown("slow", function () {
          $("#approveMessage")
            .delay(3000)
            .slideUp("slow", function () {
              $("#approveMessage").toggleClass("d-none");
              $("#approveMessage").toggleClass("alert-danger");
              $("#approveMessage p").empty();
            });
        });
      },
    });
  });
});
