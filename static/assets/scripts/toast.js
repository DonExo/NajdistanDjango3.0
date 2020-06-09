/////////////////////////// TOAST MESSAGES ///////////////////////////

let $window = $(window);
let toastEleContainer = $(".toast-container");
let toastCloseBtn = $(".toast-message-close");
let toastEle = $(".toast");

function trackToastDOMAppend() {
    const oldHtml = window.jQuery.fn.append;

    window.jQuery.fn.append = function () {
        const enhancedHtml = oldHtml.apply(this, arguments);

        if (arguments.length && enhancedHtml.find('.toast').length) {
            const toastAdded = enhancedHtml.find('.toast');
            let addToast = null;
            let autoRemoveToast = null;
            
            addToast = setTimeout(function() {
                toastAdded.addClass("toast-active");
                clearTimeout(addToast);
            }, 10);

            autoRemoveToast = setTimeout(function() {
                removeToast(toastAdded);
                clearTimeout(autoRemoveToast);
            }, 6000);
            
            return toastAdded;
        }
    }
}

function addToast ({ toastType, toastMsg }) {
    toastEleContainer
        .append(`<div class="toast">`+
                    `<div class="toast-message toast-message-${toastType}">`+
                        `<p>${toastMsg}</p>`+
                        `<div class="toast-message-close"><i class="sl sl-icon-close"></i></div>`+
                    `</div>`+
                `</div>`
    );
}

function removeToast(targetToast = toastEle) {
    let timeout;

    targetToast.removeClass("toast-active");
    //remove element after timeout
    timeout = setTimeout(function(){
        targetToast.remove();
        clearTimeout(timeout);
    }, 300);
}

toastEleContainer.on('click', $(".toast-message-close"), function (e) {
    let $eTarget = $(e.target);
    let targetToast = null;

    if($eTarget.hasClass('sl-icon-close')){
        targetToast = $eTarget.parent().parent().parent();
        removeToast(targetToast);
    }
});

// Track append event to check DOM if toast has been added
$(trackToastDOMAppend);

$window.on('load', function() {
  if(toastCloseBtn.length > 0) {
    autoRemoveToast = setTimeout(function() {
      removeToast();
      clearTimeout(autoRemoveToast);
    }, 6000);
  }
});