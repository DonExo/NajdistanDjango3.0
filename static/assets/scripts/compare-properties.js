(function($){
    "use strict";

    $(document).ready(function(){
        const compareSlideMenu = $('.compare-slide-menu');

        function retrieveLocalStorageItem (lsItem) {
            let prevLsItem = null;
    
            if ( localStorage.length !== 0 && !!localStorage[lsItem] ){
                prevLsItem = JSON.parse(localStorage.getItem(lsItem));
                return prevLsItem;
            } else {
                return false;
            }
        }
    
        function storeUniqueLocalStorageObject (props) {
            const {
                currentStorage,
                localStorageKey,
                storageObjectName,
                propSlug,
                propHref,
                propPrice,
                propThumbnail,
                propTitle,
                propType,
            } = props;

            let newPropertyObject = {}

            const propertyExists = currentStorage[storageObjectName].findIndex( item => item.propSlug === propSlug );
            
            if( propertyExists < 0 ){
                newPropertyObject = {
                    propSlug: propSlug,
                    propHref: propHref,
                    propPrice: propPrice,
                    propThumbnail: propThumbnail,
                    propTitle: propTitle,
                    propType: propType
                }
                currentStorage[storageObjectName].push(newPropertyObject);
                localStorage.setItem(localStorageKey, JSON.stringify(currentStorage));
            }
    
            return;
        }
    
        function removeSingleLocalStorageItem (lsItem) {
            if( localStorage.length !== 0 && !!localStorage[lsItem] ) {
                localStorage.removeItem(LOCALSTORAGE_KEY);
                console.log("localStorage cleared!");
            }
        }

        function populateRevealCompareContainer () {
            const { propCollection } = retrieveLocalStorageItem(LOCALSTORAGE_KEY);

            const mappedProperties = !!propCollection && propCollection.map((item) => {
                return (`<div class="listing-item compact">`+
                    `<a href="${item.propHref}" class="listing-img-container">`+
                        `<div class="remove-from-compare"><i class="fa fa-close"></i></div>`+
                        `<div class="listing-badges">`+
                            `<span>${item.propType}</span>`+
                        `</div>`+
                        `<div class="listing-img-content">`+
                            `<span class="listing-compact-title">${item.propTitle}<i>${item.propPrice}</i></span>`+
                        `</div>`+
                        `<img src="${item.propThumbnail}" alt="${item.propTitle}">`+
                    `</a>`+
                `</div>`);
            });

            compareSlideMenu.find(".csm-properties").html(mappedProperties);

            compareSlideMenu.toggleClass('active');
        }

        function removeItemFromCompareContainer (lsItem = null) {

        }
    
        const LOCALSTORAGE_KEY = 'compareProperties';
        const UNIQUE_STORAGE_OBJECT_NAME = 'propCollection';

        /*----------------------------------------------------*/
        /*  Compare Menu
        /*----------------------------------------------------*/
        $('.csm-trigger').on('click', function(){
            populateRevealCompareContainer();
        });

        $('.csm-mobile-trigger').on('click', function(){
            compareSlideMenu.removeClass('active');
        });

        // Trigger compare button
        $('.compare-button, .compare-widget-button').on('click', function(){
            const $this = $(this);
            const prevLsProperties = retrieveLocalStorageItem(LOCALSTORAGE_KEY); // Retrieve previous properties
            const storageProps = { // Prepare data to set new storage
                currentStorage: { propCollection:[] },
                localStorageKey: LOCALSTORAGE_KEY,
                storageObjectName: UNIQUE_STORAGE_OBJECT_NAME,
                propSlug: $this.data("slug"),
                propHref: $this.parent().parent().attr("href"),
                propPrice: $this.parent().children(".listing-price").text(),
                propThumbnail: $this.parent().next(".listing-carousel").find(".owl-item > div > img")[0].getAttribute("src"),
                propTitle: $this.parent().parent().next(".listing-content").find(".listing-title h4 a").text(),
                propType: $this.parent().prev(".listing-badges").children(".listing-type").text()
            }

            !!prevLsProperties && (storageProps.currentStorage = prevLsProperties); // Update LocalStorage clone

            // Store new property to compare
            if ( storageProps.currentStorage.propCollection.length <= 2 ) {
                storeUniqueLocalStorageObject(storageProps)
            } else {
                $('.compare-slide-menu .csm-message').addClass('active');
            }

            populateRevealCompareContainer();
        });

        // Remove property from compare list
        $(".remove-from-compare").on('click', function(e){
            e.preventDefault();
        });

        // Reset local storage
        $('.csm-buttons .reset').on('click', function(){
            removeSingleLocalStorageItem(LOCALSTORAGE_KEY)
            $('.compare-slide-menu .csm-message').removeClass('active');
        });
    });
})(this.jQuery);