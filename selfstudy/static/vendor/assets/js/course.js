$(document).ready(function() {
      var $grid = $('.grid').masonry({
        // options...
        itemSelector: '.grid-item',
        transitionDuration: 0,
        horizontalOrder: true
    });

    // layout Masonry after each image loads
    $grid.imagesLoaded().progress(function() {
        // init Masonry
        $grid.masonry('layout');

    })  
})