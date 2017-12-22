$(document).ready(function(){

    if ($('#id_firstName').val() != "") {
        document.getElementById('firstName').value = document.getElementById('id_firstName').value     
    }

    if ($('#id_lastName').val() != "") {
        document.getElementById('lastName').value = document.getElementById('id_lastName').value        
    }

    if ($('#id_emailAddress').val() != "") {
        document.getElementById('emailAddress').value = document.getElementById('id_emailAddress').value
    }

    if ($('#id_password').val() != "") {
        document.getElementById('password').value = document.getElementById('id_password').value
    }

    if ($('#id_confirmPassword').val() != "") {
        document.getElementById('confirmPassword').value = document.getElementById('id_confirmPassword').value
    }

    
    $("#firstName").bind('onfocusout change keyup' ,function() {
        if ($(this).val().length == 2 || $(this).val().length > 2) {
            $("#forFirstName").removeClass("has-warning");
            $(".form-control-feedback").addClass("d-none");
            $("#forFirstName").addClass("has-success");
            $(this).addClass("form-control-success");
            $("#submitBtn").removeAttr('disabled');
        } else {
            $("#forFirstName").addClass("has-warning");
            $("#forFirstName .form-control-feedback").removeClass("d-none"); 
            $(this).addClass("form-control-warning");
            $("#forFirstName").removeClass("has-success");
            $(this).removeClass("form-control-success");
            $("#submitBtn").attr('disabled', 'disabled');
        }
    })

    $("#lastName").bind('onfocusout change keyup', function() {
        if ($(this).val().length == 2 || $(this).val().length > 2) {
            $("#forLastName").removeClass("has-warning");
            $("#forLastName .form-control-feedback").addClass("d-none");
            $("#forLastName").addClass("has-success");
            $(this).addClass("form-control-success");
            $("#submitBtn").removeAttr('disabled');
        } else {
            $("#forLastName").addClass("has-warning");
            $("#forLastName .form-control-feedback").removeClass("d-none"); 
            $(this).addClass("form-control-warning");
            $("#forLastName").removeClass("has-success");
            $(this).removeClass("form-control-success");
            $("#submitBtn").attr('disabled', 'disabled');
        }
    })

    $("#emailAddress").bind('change keyup', function() {
        var email = $(this).val();
        var res = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email);
        if (res) {
            $("#forEmail").removeClass("has-warning");
            $("#forEmail .form-control-feedback").addClass("d-none");
            $("#forEmail").addClass("has-success");
            $(this).addClass("form-control-success");
        } else {
            $("#forEmail").addClass("has-warning");
            $("#forEmail .form-control-feedback").removeClass("d-none"); 
            $(this).addClass("form-control-warning");
            $("#forEmail").removeClass("has-success");
            $(this).removeClass("form-control-success");
            $("#submitBtn").attr('disabled', 'disabled');
        }
    })

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
