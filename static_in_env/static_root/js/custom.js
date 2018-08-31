// PREVENT ENTER KEY ON ALL INPUT & BUTTON
// CAN ONLY TRIGGERED THRU CLICK EVENT
// $(document).ready(function() {
//   $(window).keydown(function(event){
//     if(event.keyCode == 13) {
//       event.preventDefault();
//       return false;
//     }
//   });
// });


function showFlashMessage(message) {
  // var template = "{% include 'alert.html' with message='" + message + "' %}"
  var template = "<div class='container container-flash-alert'>" + 
  "<div class='col-sm-3 col-sm-offset-8'> " + 
  "<div class='alert alert-success alert-dismissible' role='alert'>" + 
  "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
  "<span aria-hidden='true'>&times;</span></button>" 
  + message + "</div></div></div>"
  $("body").append(template);
  $(".container-flash-alert").fadeIn();
  setTimeout(function(){ 
    $(".container-flash-alert").fadeOut();
  }, 1800);

}