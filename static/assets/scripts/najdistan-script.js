function generateListingData() {
    var title = document.getElementById('id_title');
    title.value = "Title #" + Math.floor(1000 + Math.random() * 9000);

    var description = document.getElementById('id_description');
    description.value = "Description #" + Math.floor(1000 + Math.random() * 9000);

    var city = document.getElementById('id_city');
    city.value = Math.floor(1 + Math.random() * 7);

    var zip_code = document.getElementById('id_zip_code');
    random1000 = Math.floor(1000 + Math.random() * 9000);
    zip_code.value = random1000 + "AB";

    var quadrature = document.getElementById('id_quadrature');
    quadrature.value = Math.floor(50 + Math.random() * 100);

    var rooms = document.getElementById('id_rooms');
    rooms.value = Math.floor(2 + Math.random() * 3);

    var bedrooms = document.getElementById('id_bedrooms');
    bedrooms.value = Math.floor(1 + Math.random() * 3);

    var floor = document.getElementById('id_floor');
    floor.value = Math.floor(1 + Math.random() * 8);

    var heating = document.getElementById('id_heating');
    heating.value = 'central'

    var price = document.getElementById('id_price');
    price.value = random1000;
}


function stickySideMenuInit($footer) {
  let sideMenu = $(".my-account-nav-container"),
      top_of_element = $footer.offset().top + 120,
      bottom_of_element = $footer.offset().top + $footer.outerHeight(),
      bottom_of_screen = $(window).scrollTop() + $(window).innerHeight(),
      top_of_screen = $(window).scrollTop() ;

  if ((bottom_of_screen > top_of_element) && (top_of_screen < bottom_of_element)) {
    sideMenu.hasClass("side-menu-sticky") && sideMenu.removeClass("side-menu-sticky");
  } else {
    if (!sideMenu.hasClass("side-menu-sticky")) {
      sideMenu.addClass("side-menu-sticky");
    }
  }
}

$(window).on("scroll", function(){
  stickySideMenuInit($(".footer-shadow"));
});

let $window = $(window);
let toastEle = $(".toast");
let toastCloseBtn = $(".toast-message-close");

function removeToast($this) {
  //let toastEle = $this.parent().parent();
  let timeout;
  toastEle.addClass("toast-hidden");
  //remove element after timeout
  timeout = setTimeout(function(){
    toastEle.remove();
    clearTimeout(timeout);
  }, 1000);
}

toastCloseBtn.on('click', function () {
  removeToast();
});

$window.on('load', function() {
  if(toastCloseBtn.length > 0) {
    autoRemoveToast = setTimeout(function() {
      removeToast();
      clearTimeout(autoRemoveToast);
    }, 6000);
  }
});




// DROPZONE
// Dropzone.autoDiscover = false;
//
// let $_dropzoneHost = $("#propertyUploadImages2");
//
// if(!!$_dropzoneHost.length){
//   let propertyImg = new Dropzone("#propertyUploadImages2", {
//       // headers: {
//       //     'x-csrf-token': $('input[name="csrfmiddlewaretoken"]').attr('value')
//       // },
//       url: "/listings/create/",
//       paramName: "images",
//       uploadMultiple: true,
//       maxFiles: 15,
//       maxFilesize: 3, // MB
//       parallelUploads: 15,
//       acceptedFiles: 'image/*',
//       addRemoveLinks: true,
//       autoProcessQueue: false,
//   });
//
//   $('#sabmit').on("click", function(e) {
//       // e.stopPropagation();
//       // e.preventDefault();
//       propertyImg.processQueue();
//   });
//
//   propertyImg.on("addedfile", function(file) {
//     file.previewElement.addEventListener("click", function() {
//       propertyImg.removeFile(file);
//     });
//   });
// }
