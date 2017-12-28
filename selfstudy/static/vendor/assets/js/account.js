$(document).ready(function(){

    $('.btn-clip').popover({
        trigger: 'click',
        html: true
    });

    $('.password-toggle').click(function() {
        $('#password').togglePassword();
        if ($("#password").hasClass("hideShowPassword-shown")) {
            $('.password-toggle').html('Hide')
        } else {
            $('.password-toggle').html('Show')
        }
    })

    new Clipboard('.btn-clip');
    
});