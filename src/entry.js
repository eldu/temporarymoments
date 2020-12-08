import { photos } from "./photos.js"

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
    // optionName: 'option value'
    // for example:
    index: 0 // start at first slide
};

// Initializes and opens PhotoSwipe on thumbnail click
(function($) {
  var	$window = $(window);
  $window.on('load', function() {
    $('#thumbs img').click(function() {
      var index = $(this).data("indexNumber");
      options.index = index;
      var gallery = new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, items, options);
      gallery.init();
    })
  });

  $('.pswp__button--caption').click(function() {
    $(this).find('i').toggleClass('fas far');
    $(".pswp__caption__real").toggleClass('close');
  });
})(jQuery);