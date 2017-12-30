$(document).ready(function(){

    $("#password").bind('change keyup', function() {
        var password = $(this).val();
        var res = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/.test(password);
        if (res) {
            $("#forPassword").removeClass("has-warning");
            $("#forPassword .form-control-feedback").addClass("d-none");
            $("#forPassword").addClass("has-success");
            $(this).addClass("form-control-success");
            $("#submitBtn").removeAttr('disabled');
        } else {
            $("#forPassword").addClass("has-warning");
            $("#forPassword .form-control-feedback").removeClass("d-none"); 
            $(this).addClass("form-control-warning");
            $("#forPassword").removeClass("has-success");
            $(this).removeClass("form-control-success");
            $("#submitBtn").attr('disabled', 'disabled');
        }
    })
    
    $("#confirmPassword, #password").bind('change keyup', function() {
        if ($("#confirmPassword").val() == $("#password").val()) {
            $("#forConfirmPassword").removeClass("has-warning");
            $("#forConfirmPassword .form-control-feedback").addClass("d-none");
            $("#forConfirmPassword").addClass("has-success");
            $("#confirmPassword").addClass("form-control-success");
            $("#submitBtn").removeAttr('disabled');
        } else {
            $("#forConfirmPassword").addClass("has-warning");
            $("#forConfirmPassword .form-control-feedback").removeClass("d-none"); 
            $("#confirmPassword").addClass("form-control-warning");
            $("#forConfirmPassword").removeClass("has-success");
            $("#confirmPassword").removeClass("form-control-success");
            $("#submitBtn").attr('disabled', 'disabled');
        }
    })

})
