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
            $("#submitBtn").removeAttr('disabled');
        } else {
            $("#forEmail").addClass("has-warning");
            $("#forEmail .form-control-feedback").removeClass("d-none"); 
            $(this).addClass("form-control-warning");
            $("#forEmail").removeClass("has-success");
            $(this).removeClass("form-control-success");
            $("#submitBtn").attr('disabled', 'disabled');
        }
    })

    $("#clientQuery").bind('change keyup', function() {
        if ($(this).val().length > 0) {
            $("#forQuery").removeClass("has-warning");
            $("#forQuery .form-control-feedback").addClass("d-none");
            $("#forQuery").addClass("has-success");
            $(this).addClass("form-control-success");
            $("#submitBtn").removeAttr('disabled');
        } else {
            $("#forQuery").addClass("has-warning");
            $("#forQuery .form-control-feedback").removeClass("d-none"); 
            $(this).addClass("form-control-warning");
            $("#forQuery").removeClass("has-success");
            $(this).removeClass("form-control-success");
            $("#submitBtn").attr('disabled', 'disabled');
        }
    })

})
