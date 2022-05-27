// close message
function closeMessage() {
  var message = document.getElementById("message");

  message.classList.add("d-none");
}
function closeFlagMessage() {
  var flagMessage = document.getElementById("flagMessage");

  flagMessage.classList.toggle("d-none");
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
// show flag popup
function flag(term_id) {
  var blur = document.getElementById("blur");
  var blur2 = document.getElementById("blur2");

  blur.classList.toggle("active");
  blur2.classList.toggle("active");

  var flagPopup = document.getElementById("flagPopup");
  flagPopup.classList.toggle("active");

  var term_id = term_id;

  return term_id

};

$(document).ready(function () {
  // applicant dropdown button
  $(".dropdown-toggle").dropdown();
  $().dropdown("hide");
  $(".Search").focus();

  // Vote functionality
  function vote() {
    var csrf = $("input[name=csrfmiddlewaretoken]").val();

    function voteForm(csrf, term_id, button) {
      $.ajax({
        url: "",
        type: "post",
        data: {
          csrfmiddlewaretoken: csrf,
          term_id: term_id,
          button: button,
          form: "vote",
        },
        // change vote count from server
        success: function (response) {
          var data = JSON.parse(response["data"]);
          var upvote = data["num_upvotes"];
          var downvote = data["num_downvotes"];

          $(".fa-thumbs-up." + term_id).text(" " + upvote);
          $(".fa-thumbs-down." + term_id).text(" " + downvote);
        },
      });
    };

    // check to see which button is clicked
    $(".thumbsUp, .thumbsDown").on("click", function (e) {
      e.preventDefault();

      // check if user is logged in so as to set session variable on click
      var logged = $(".vote button").attr("onclick");

      if (logged === "vote();") {
        // Send data according to clicked button
        var button = this.getAttribute("aria-label");

        if (button === "upVote") {
          var term_id = this.getAttribute("data-termid");
          var button = "upVote";
          // submit form
          voteForm(csrf, term_id, button);

          // downvote functionality
        } else if (button === "downVote") {
          var term_id = this.getAttribute("data-termid");
          var button = "downVote";
          // submit form
          voteForm(csrf, term_id, button);
        }
      } else if (logged === "login();") {
        // send form to set session variable for clicked button to change after log in
        
        if (button === "upVote") {
          var term_id = this.getAttribute("data-termid");

          // submit form
          $.ajax({
            url: "",
            type: "get",
            data: {
              term_id: term_id,
              button: "upVote",
            },
          });

          // downvote functionality
        } else if (button === "downVote") {
          var term_id = this.getAttribute("data-termid");

          // submit form
          $.ajax({
            url: "",
            type: "get",
            data: {
              term_id: term_id,
              button: "downVote",
            },
          });
        }
      }
    });
  }

  vote();

  function report() {
    var csrf = $("#flagPopup input[name=csrfmiddlewaretoken]").val();


    // show other reason text area if other is selected
    $("#flagReason").on("click", function () {
      var reason = $("#flagReason").val();
      var element = $("#other_reason");

      if (reason === "Other") {
        element.removeClass("d-none");
      } else {
        element.addClass("d-none");
      }
    });

    $("#btnReport").on("click", (e) => {
      e.preventDefault();
      var reason = $("#flagReason").val();
      var other_reason = $("#other_reason").val();
      var term_id = $("#btn-flag").attr("data-termid");

      $.ajax({
        url: "",
        type: "post",
        data: {
          csrfmiddlewaretoken: csrf,
          term_id: term_id,
          reason: reason,
          other_reason: other_reason,
          form: "flag",
        },
        success: function (response) {
          var data = JSON.parse(response["data"]);
          var message = data["message"];

          $("#flagMessage." + term_id).removeClass("d-none");
          $(".messageDisplay." + term_id).text(message);
        },
      });

      // close flag popup
      flag();
    });
  }
  report();
});

// function vote() {
//   // check to see which button is clicked
//   $(".thumbsUp, .thumbsDown").on("click", function (e) {
//     e.preventDefault();
//     var button = this.getAttribute('aria-label');

//     if (button === "upVote") {
//       console.log("up");
//       var term_id = this.getAttribute('data-termid');
//       console.log(term_id);
//     } else if (button === "downVote") {
//       console.log("down");
//     }
//   });
// };
// vote()
 