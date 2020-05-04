function generateListingData() {
    var title = document.getElementById('id_title');
    title.value = "Title #" + Math.floor(1000 + Math.random() * 9000);

    var description = document.getElementById('id_description');
    description.value = "Description #" + Math.floor(1000 + Math.random() * 9000);

    var city = document.getElementById('id_city');
    city.value = Math.floor(2 + Math.random() * 7);

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


let toastClose = $(".toast-message-close");

toastClose.on('click', function () {
  let thisToast = $(this).parent().parent();
  //remove element after timeout
  let timeout;
  thisToast.addClass("toast-hidden");
  timeout = setTimeout(function(){
    thisToast.remove();
    clearTimeout(timeout);
  }, 1000);
});


Dropzone.autoDiscover = false;

propertyImg = new Dropzone("#propertyUploadImages", {
    headers: {
        'x-csrf-token': $('input[name="csrfmiddlewaretoken"]').attr('value')
    },
    url: ".",
    paramName: "images", // The name that will be used to transfer the file
    dictDefaultMessage: "<i class='sl sl-icon-plus'></i> Click here or drop files to upload",
    dictResponseError: 'Error uploading file!',
    uploadMultiple: true,
    maxFiles: 5,
    maxFilesize: 2, // MB
    acceptedFiles: 'image/*',
    addRemoveLinks: true
});

propertyImg.on("addedfile", function(file) {
  file.previewElement.addEventListener("click", function() {
    propertyImg.removeFile(file);
  });
});