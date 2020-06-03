(function($){
    "use strict";

    $(document).ready(function(){
        const compareSlideMenu = $(".compare-slide-menu");
        const compareProperties = $(".csm-properties");
        const LOCALSTORAGE_KEY = 'compareProperties';
        const UNIQUE_STORAGE_OBJECT_NAME = 'propCollection';

        function retrieveLocalStorageItem (lsKey) {
            let lsCollection = null;
    
            if ( localStorage.length !== 0 && !!localStorage[lsKey] ){
                lsCollection = JSON.parse(localStorage.getItem(lsKey));
                return lsCollection;
            } else {
                return false;
            }
        }

        function addLocalStorageItem ( lsKey, lsItem ) {
            removeLocalStorageItem( lsKey );
            localStorage.setItem( lsKey, JSON.stringify(lsItem) );
        }
    
        function removeLocalStorageItem ( lsKey ) {
            if ( localStorage.length !== 0 && !!localStorage[lsKey] ) {
                localStorage.removeItem( lsKey );
                console.log("localStorage cleared!");
            } 
        }

        function collectAndStoreProperties (props) {
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
                addLocalStorageItem(localStorageKey, currentStorage);
            }
    
            return;
        }

        function populateCompareContainer () {
            const { propCollection } = retrieveLocalStorageItem(LOCALSTORAGE_KEY);

            const mappedProperties = !!propCollection && propCollection.map((item) => {
                return (`<div class="listing-item compact">`+
                    `<a href="${item.propHref}" class="listing-img-container">`+
                        `<div class="remove-from-compare" data-prop-slug="${item.propSlug}"></div>`+
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

            compareProperties.html(mappedProperties);
        }

        function removeProperty (lsSlug) {
            const oldPropCollection = retrieveLocalStorageItem( LOCALSTORAGE_KEY );
            const currentStorage = { propCollection:[] };

            currentStorage.propCollection = oldPropCollection.propCollection.filter( item => item.propSlug !== lsSlug );
            addLocalStorageItem(LOCALSTORAGE_KEY, currentStorage);
        }

        /*----------------------------------------------------*/
        /*  Compare Menu
        /*----------------------------------------------------*/
        $('.csm-trigger').on('click', function(){
            compareSlideMenu.toggleClass('active');
            populateCompareContainer();
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
                collectAndStoreProperties(storageProps)
            } else {
                $('.compare-slide-menu .csm-message').addClass('active');
            }

            populateCompareContainer();
            !compareSlideMenu.hasClass('active') && compareSlideMenu.addClass('active');
        });

        // Remove property from compare list
        compareProperties.on('click', $(".remove-from-compare"), function(e){
            let propSlug = e.target.getAttribute('data-prop-slug');
            
            if(propSlug) {
                e.preventDefault();
                removeProperty(propSlug);
                $(e.target.parentNode.parentNode).remove();
            }
        });

        // Reset local storage
        $('.csm-buttons .reset').on('click', function(){
            removeLocalStorageItem(LOCALSTORAGE_KEY)
            $(".listing-item.compact").remove();
            $('.compare-slide-menu .csm-message').removeClass('active');
        });
    });
})(this.jQuery);