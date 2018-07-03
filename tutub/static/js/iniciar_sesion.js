$(function() {
    $("#form").submit(function( event ) {
        if($("#username").val().trim()=== "") {
            event.preventDefault()
            $("#username").addClass('is-invalid');
            $(" <p id='error_1_id_username' class='invalid-feedback'><strong>Este campo es requerido</strong></p>" ).insertAfter("#username");
            
      }   
      });
});



