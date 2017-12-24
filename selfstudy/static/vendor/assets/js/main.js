$(document).ready(function(){

$('#cd-menu-trigger, main').click(function() {
    if ($('#cd-menu-trigger').hasClass('is-clicked')) {
        $('#cd-menu-trigger').css('background-color', 'rgb(235,148,79)');
    } else {
        $('#cd-menu-trigger').css('background-color', 'rgb(28,78,200)');
    }
})

$('#hide-cart').click(function() {
    $(".wrap-cart").animate({left: "-500px"});
});

$('#show-cart').click(function() {
    $(".wrap-cart").animate({left: "-2px"});
});

$('#submit-form').click(function() {
    $(this).prop("disabled")
})

});