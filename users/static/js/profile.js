$(document).ready(() => {
  $(".dropdown-toggle").dropdown();
});

// close message
$("#closeMessage").click(function (){
    $("#message").fadeOut("slow");
})