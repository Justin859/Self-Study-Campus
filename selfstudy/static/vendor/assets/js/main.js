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

$('#DropDownAccount').on('hidden.bs.collapse', function () {
    $('#faq').removeClass('hidden-sm-down');
    $('#tc').removeClass('hidden-sm-down');
    $('#caret-position').addClass('fa-caret-down');
    $('#caret-position').removeClass('fa-caret-up');
});

$('#DropDownAccount').on('show.bs.collapse', function () {
    $('#faq').addClass('hidden-sm-down');
    $('#tc').addClass('hidden-sm-down');
    $('#caret-position').addClass('fa-caret-up');
    $('#caret-position').removeClass('fa-caret-down');
})

if($("#view-more")) {
    $("#more-orders").hide()
    $("#view-more").click(function() {
        $("#more-orders").toggle()
    });
}

$('#show-cart, #hide-cart').click(function(event) {
    event.preventDefault();
})

$(".addToCart").click(function() {
    $(this).prop('disabled', true);
    $(this).html('Added to Cart&nbsp;&nbsp;<i class="fa fa-shopping-cart"></i>');
    $(this).removeClass('btn-secondary');
    $(this).addClass('btn-primary');
    var price = parseInt($(this).data("price"))

    var totalCost = parseFloat($("#cart-total-cost").text()) + price
    var totalItems = parseFloat($("#cart-total-items").text()) + 1
    $("#cart-total-cost").html(totalCost + '.00');
    $("#cart-total-items").html(totalItems)
});

});

var AddToCart = function(item_id, user_id) {

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/add-to-cart/",
        data: { user_id: user_id, item_id: item_id },
        success: function() {
            console.log("Added to cart");
        },
    })

};
