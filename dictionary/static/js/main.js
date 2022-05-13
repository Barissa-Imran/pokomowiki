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
});
