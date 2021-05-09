import { photos } from "./photos.js"
import Masonry from 'masonry-layout';
import ImagesLoaded from 'imagesloaded';

/*
  MASONRY
*/
var grid = document.querySelector('.grid');

var msnry = new Masonry( grid, {
  itemSelector: 'none', // select none at first
  columnWidth: '.grid__col-sizer',
  percentPosition: true,
  transitionDuration: 0,
});

var imagesLoaded = new ImagesLoaded( grid, function(){
  grid.classList.remove('are-images-unloaded');
  msnry.options.itemSelector = '.grid__item';
  var items = grid.querySelectorAll('.grid__item');
  msnry.appended( items );
});

/*
  PHOTOSWIPE
*/
var pswpElement = document.querySelectorAll('.pswp')[0];

// build items array
var items = new Array(photos.length);
for (var i = 0; i < photos.length; i++) {
  var p = photos[i];
  items[i] = {
    src: "images/photos_fullsize/".concat(p["id"]).concat(".").concat(p["fileExtension"]),
    w: p["imageMediaMetadata"]["width"],
    h: p["imageMediaMetadata"]["height"],
    title: p["description"]
  };
}

// define options (if needed)
var options = {
    index: 0, // start at first slide
    closeOnScroll: false,
    closeOnVerticalDrag: false
};

// Initializes and opens PhotoSwipe on thumbnail click
(function($) {
  var	$window = $(window);
  $window.on('load', function() {
    $('#gallery .grid__item').click(function() {
      var index = $(this).data("indexNumber");
      options.index = index;
      var gallery = new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, items, options);
      gallery.init();
    })
  });

  $('.pswp__button--caption').click(function() {
    $(this).find('i').toggleClass('fas far');
    $(".pswp__caption").toggleClass('pswp__caption__hide');
  });
})(jQuery);