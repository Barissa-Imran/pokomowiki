// close message
function closeMessage() {
  var message = document.getElementById("message");

  message.classList.add("d-none");
}

// show login popup
function login() {
  var blur = document.getElementById("blur");
  var blur2 = document.getElementById("blur2");

  blur.classList.toggle("active");
  blur2.classList.toggle("active");

  var popup = document.getElementById("popup");
  popup.classList.toggle("active");
}



$(document).ready(function () {
  // applicant dropdown button
  $(".dropdown-toggle").dropdown();
  $(".Search").focus();

  // Vote functionality
  function vote() {
    // check to see which button is clicked
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    // let isSubmit = false;

    $("#upVote, #downVote").on('click',function (e) {
      e.preventDefault();

      if (this.id === "upVote") {
        var term_id = $("#upVote").attr("data-termid");
        // submit form
        e.preventDefault();

        $.ajax({
          url: "",
          type: "post",
          data: {
            csrfmiddlewaretoken: csrf,
            term_id: term_id,
            button: "upVote",
          },
          // change vote count from server
          success: function (response) {
            var data = JSON.parse(response["data"]);
            var upvote = data["term"];
            $(".fa-thumbs-up").text(upvote);
          },
        });
      } else if (this.id === "downVote") {
        var term_id = $("#downVote").attr("data-termid");
        e.preventDefault();

        $.ajax({
          url: "",
          type: "post",
          data: {
            csrfmiddlewaretoken: csrf,
            term_id: term_id,
            button: "downVote",
          },
          // change vote count from server
          success: function (response) {
            var data = JSON.parse(response["data"]);
            var downvote = data["term"];
            $(".fa-thumbs-down").text(downvote);
          },
        });
      }
    });
  }
  vote();
  function flag() {
    // show flag pop up
    // submit form
    // show message success
  }
  flag();
});
