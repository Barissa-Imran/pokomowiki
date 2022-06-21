$(document).ready(() => {
  // bs dropdown functionality
  $(".dropdown-toggle").dropdown();

  // close message after delay if available
  var $messageBox = $("#message");
  if ($.contains(document, $messageBox[0])) {
    $messageBox.delay(3000).slideUp("slow", () => {
      $messageBox.addClass("d-none");
    });
  } else {
    //pass
  }

  // Show confirm delete dialog
  $("#deleteAcc").on("click", function () {
    $("#deletePopup").fadeIn("slow", function () {
      $("#deletePopup").removeClass("d-none");
    });
  });

  // hide confirm delete dialog
  $("form #cancel").on("click", function () {
    $("#deletePopup").toggleClass("d-none");
  });

  // submit username in delete user dialog
  $("#deletePopup").submit((e) => {
    e.preventDefault();

    const username = $("#confirm").val();
    const csrf = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      url: "",
      type: "post",
      data: {
        username: username,
        csrfmiddlewaretoken: csrf,
      },
      success: (response) => {
        document.getElementById("deletePopup").reset();
        var data = JSON.parse(response["data"]);
        console.log(data);
      },
      error: (response) => {
        document.getElementById("deletePopup").reset();
        var data = JSON.parse(response.responseJSON["data"]);

        $("#approveMessage").toggleClass("d-none");
        $("#approveMessage").toggleClass("alert-danger");
        $("#approveMessage p").prepend(data["msg"]);

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
function complete() {
  $("#message").addClass(d - none);
}

// close message fallback if delay fails
$("#closeMessage").click(function () {
  $("#message").fadeOut("slow", complete);
});
