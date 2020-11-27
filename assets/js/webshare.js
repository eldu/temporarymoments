const shareButton = document.querySelector('.share-button');
const shareDialog = document.querySelector('.share-dialog');
const closeButton = document.querySelector('.close-button');

shareButton.addEventListener('click', event => {
  if (navigator.share) {
   navigator.share({
      title: 'Temporary Moments',
      url: 'https://www.temporarymoments.com/'
    }).then(() => {
      console.log('Thanks for sharing!');
    })
    .catch(console.error);
    } else {
        shareDialog.classList.add('is-open');
    }
});

closeButton.addEventListener('click', event => {
  shareDialog.classList.remove('is-open');
});

function copyText() {
  // Get the text field
  var copyText = document.getElementById("copy-url");

  // Select the text field
  copyText.select();
  copyText.setSelectionRange(0, 99999);

  // Copy the text inside the text field
  document.execCommand("copy");

  // Update tooltip
  var tooltip = $("#tooltiptext");
  tooltip.css('opacity', 0.9);
  tooltip.show();
  tooltip.fadeOut("fast", "swing");
}

function popupWindow(url, winWidth, winHeight) {
  // TODO: Add in default image when sharing
  var winTop = Math.max(screen.height / 2.0 - winHeight / 2.0, 0.0);
  var winLeft = Math.max(screen.width / 2.0 - winWidth / 2.0, 0.0);

  var options = 'menubar=no,toolbar=no,location=no,resizable=yes,scrollbars=yes'
    + ',width=' + winWidth + ',height=' + winHeight
    + ',top=' + winTop + ',left=' + winLeft;
  window.open(url, '', options);
}