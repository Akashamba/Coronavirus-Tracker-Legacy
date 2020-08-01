mybutton = document.getElementById("myBtn");

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

function topFunction() {
  document.body.scrollTop = 0; 
  document.documentElement.scrollTop = 0; 
}

function shareLarge() {
  var copyText = document.getElementById("copy-data");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  document.execCommand("copy");
}

function shareSmall() {
  var copyText = document.getElementById("copy-data-2");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  document.execCommand("copy");
  alert("Copied the text: " + copyText.value);
}

function openNav() {
  document.getElementById("mySidenav").style.width = "60vw";
  document.getElementById("mySidenav").style.boxShadow = "0 .5rem 1rem .5rem rgba(0,0,0,.2)";
  document.getElementsByTagName("body")[0].onclick="closeNav()";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("mySidenav").style.boxShadow = "0 .5rem 1rem .5rem rgba(0,0,0,0)";
  document.getElementsByTagName("body")[0].onclick="";
}

const shareButton = document.querySelector('.share-button');
const shareDialog = document.querySelector('.share-dialog');
const closeButton = document.querySelector('.close-button');

shareButton.addEventListener('click', event => {
  if (navigator.share) { 
   navigator.share({
      title: 'Coronavirus Live Tracker',
      url: 'https://coronavirus-live-tracker.herokuapp.com/'
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
