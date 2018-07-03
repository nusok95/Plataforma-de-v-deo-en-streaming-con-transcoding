


$(function() {
    $("#registro").on("submit",function(event){
        if($("#password").val().trim()=== ""){
            alert("weon no puedes hacer eso")
            event.preventDefault();
            $("#password").css('border', '5px solid red');
            //$('#falloTexto').toggle();
            $('#error').fadeIn(500).fadeOut(5000);
        }
    });
});



// $("#registro").submit(function(){
//     alert("que pedo compa");
//     jQuery.validator.setDefaults({
//         debug: true,
//         success: "valid"
//     });
    
//     // function to validate first password
    
//     $.validator.addMethod("pwcheck", function(value) {
//     return /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/.test(value)
//     });
    
//     $( "#registro" ).validate({
//         rules: {
//         password:{
//         required:true,
//         minlength:8,
//         pwcheck:true
//         },
//         password_again:{
//         minlength:8,
//         equalTo :'#Password'
//         }
//         }
//     });
// });