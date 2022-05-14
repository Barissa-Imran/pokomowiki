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

// Vote functionality
function vote() {
  // check to see which button is clicked
  var csrf = $("input[name=csrfmiddlewaretoken]").val();
  let isSubmit = false;
  var term_id = $("#upVote").attr("data-termid");
  console.log(term_id);

  $("#upVote, #downVote").click(function () {
    if (this.id === "upVote") {
      var term_id = $("#upVote").attr("data-termid");
      $("vote").submit(function (e) {
        e.preventDefault();
        if (isSubmit) {
          return;
        }
        isSubmit = true;

        $.ajax({
          url: "",
          type: "post",
          data: {
            csrfmiddlewaretoken: csrf,
            term_id: term_id,
            button: "upVote",
          },
        });
      });
    } else if (this.id === "downVote") {
      console.log("downVote");
    }
  });

  // submit form
  // change vote count from server
}
vote();
function flag() {
  // show flag pop up
  // submit form
  // show message success
}
flag();

$(document).ready(function () {
  // applicant dropdown button
  $(".dropdown-toggle").dropdown();
  $(".Search").focus();
});
