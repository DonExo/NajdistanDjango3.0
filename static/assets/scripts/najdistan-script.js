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

    var construction = document.getElementById('id_construction_year');
    random2000 = Math.floor(2000 + Math.random() * 20);
    construction.value = random2000;
}


///////////////////////////// STICKY SIDEMENU (WIP) ///////////////////////////
(function($){
    "use strict";

    $(document).ready(function(){
        function stickySideMenuInit(sticky, controlRef, sOffset) {
            let screenTop = Math.round($(window).scrollTop()), // returns number
                doubleOffset = 2*sOffset,
                newPositionOfSticky = screenTop - sticky.top + doubleOffset,
                stopPoint = controlRef.bottom - sticky.eleHeight - doubleOffset;

            if (stopPoint < screenTop) {
                sticky.element.css({ top: `${stopPoint - (sOffset)}px` });
            } else if (sticky.top < screenTop + doubleOffset) {
                sticky.element.css({ top: `${newPositionOfSticky}px` });
            } else {
                sticky.element.css({ top: 0 });
            }
        }

        const mainContent = $(".main-content"),
            mainContentHeight = mainContent.outerHeight(),
            stickyOffset = 65,
            $window = $(window),
            windowWidth = $window.innerWidth(),
            windowBreakpoint = 992;

        const controlRef = {
            element: $(".main-content"),
            top: Math.round($(".main-content").offset().top),
            bottom: Math.round($(".main-content").offset().top + $(".main-content").outerHeight())
        }
        
        const sticky = {
            element: $(".sidebar.left"),
            top: Math.round($(".sidebar.left").offset().top),
            eleHeight: $(".sidebar.left").outerHeight()
        }

        let throttleStickyScroll =  _.throttle(
            function(){
                stickySideMenuInit(sticky, controlRef, stickyOffset)
            }, 100, { 'leading': true });

        if ( mainContentHeight > sticky.eleHeight && windowWidth > windowBreakpoint ) {
            sticky.element.addClass("sticky");
            $window.on('scroll', throttleStickyScroll);
        }

    });

})(this.jQuery);

/////////////////////////// DROPZONE ///////////////////////////
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
