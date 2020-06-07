(function($){
    "use strict";

    $(document).ready(() => {
        const $window = $(window);
        const compareSlideMenu = $(".compare-slide-menu");
        const compareProperties = $(".csm-properties");
        const LOCALSTORAGE_KEY = 'compareProperties';
        const UNIQUE_STORAGE_OBJECT_NAME = 'propCollection';

        let retrieveLocalStorageItem = ( lsKey ) => {
            let lsCollection = null;
    
            if ( localStorage.length !== 0 && !!localStorage[lsKey] ){
                lsCollection = JSON.parse(localStorage.getItem(lsKey));
                return lsCollection;
            } else {
                return false;
            }
        }

        let addLocalStorageItem = ( lsKey, lsItem ) => {
            removeLocalStorageItem( lsKey );
            localStorage.setItem( lsKey, JSON.stringify(lsItem) );
        }
    
        let removeLocalStorageItem = ( lsKey ) => {
            if ( localStorage.length !== 0 && !!localStorage[lsKey] ) {
                localStorage.removeItem( lsKey );
                console.log("localStorage cleared!");
            } 
        }

        let collectAndStoreProperties = (props) => {
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

            let propCollection = {}

            const propertyExists = currentStorage[storageObjectName].findIndex( item => item.propSlug === propSlug );
            
            if( propertyExists < 0 ){
                propCollection = {
                    propSlug: propSlug,
                    propHref: propHref,
                    propPrice: propPrice,
                    propThumbnail: propThumbnail,
                    propTitle: propTitle,
                    propType: propType
                }
                currentStorage[storageObjectName].push(propCollection);
                addLocalStorageItem(localStorageKey, currentStorage);
                populateCompareContainer(propCollection);
            }
    
            return;
        }

        let populateCompareContainer = ( propItem = null ) => {
            const propText = {
                propCollection: [propItem]
            }
            const { propCollection } = propItem ? propText : retrieveLocalStorageItem(LOCALSTORAGE_KEY);
            const mappedProperties = !!propCollection && propCollection.map((item) => {
                return (`<div class="listing-item compact inactive">`+
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
                    `</div>`
                );
            });

            compareProperties.append(mappedProperties);

            propItem && 
                compareProperties.children(".listing-item:last-child").animate({ marginLeft: '0' }, 200);
        }

        let removeProperty = (lsSlug) => {
            const oldPropCollection = retrieveLocalStorageItem( LOCALSTORAGE_KEY );
            const currentStorage = { propCollection:[] };

            currentStorage.propCollection = oldPropCollection.propCollection.filter( item => item.propSlug !== lsSlug );
            addLocalStorageItem(LOCALSTORAGE_KEY, currentStorage);
        }

        let setQueryString = () => {
            let qString = '';
            const { propCollection } = retrieveLocalStorageItem(LOCALSTORAGE_KEY);
            propCollection.map(( item ) => {
                return qString += `c=${item.propSlug}&`;
            });

            return qString;
        }

        /*----------------------------------------------------*/
        /*  Compare Menu
        /*----------------------------------------------------*/
        $('.csm-trigger').on('click', () => {
            compareSlideMenu.toggleClass('active');
            compareProperties.children(".listing-item.compact").removeClass("inactive");
        });

        $('.csm-mobile-trigger').on('click', () => {
            compareSlideMenu.removeClass('active');
        });

        // Trigger set compare button
        $('.compare-button, .compare-widget-button').on('click', function () {
            const $this = $(this);
            const prevLsProperties = retrieveLocalStorageItem(LOCALSTORAGE_KEY); // Retrieve previous properties
            // const storageProps = { // Prepare data to set new storage
            //     currentStorage: { propCollection:[] },
            //     localStorageKey: LOCALSTORAGE_KEY,
            //     storageObjectName: UNIQUE_STORAGE_OBJECT_NAME,
            //     propSlug: $this.data("slug"),
            //     propHref: $this.parent().parent().attr("href"),
            //     propPrice: $this.parent().children(".listing-price").text(),
            //     propThumbnail: $this.parent().next(".listing-carousel").find(".owl-item > div > img")[0].getAttribute("src"),
            //     propTitle: $this.parent().parent().next(".listing-content").find(".listing-title h4 a").text(),
            //     propType: $this.parent().prev(".listing-badges").children(".listing-type").text()
            // }

            $.ajax({
                type: "POST",
                url: `/listings/get_json_data/`,
                async: true,
                dataType: "json",
                data: {"propSlug": $this.data("slug")},
                success: function(response){
                    console.log(response);
                },
                error: function(xhr, status, err) {
                    console.log(err);
                },
                complete: function(){
                    console.log('data pull complete');
                }
            });

            compareProperties.children(".listing-item.compact").removeClass("inactive");
            
            !!prevLsProperties && (storageProps.currentStorage = prevLsProperties); // Update LocalStorage clone

            // Store new property to compare
            if ( storageProps.currentStorage.propCollection.length <= 2 ) {
                collectAndStoreProperties(storageProps)
            } else {
                $('.compare-slide-menu .csm-message').addClass('active');
            }

            !compareSlideMenu.hasClass('active') && compareSlideMenu.addClass('active');
            
        });

        // Remove property from compare list
        compareProperties.on('click', $(".remove-from-compare"), (e) => {
            let propSlug = e.target.getAttribute('data-prop-slug');
            
            if(propSlug) {
                e.preventDefault();
                removeProperty(propSlug);

                $(e.target.parentNode.parentNode).animate({ marginLeft: '120%' }, 200, function(){
                    $(e.target.parentNode.parentNode).remove();
                });
            }
        });

        // Reset local storage
        $('.csm-buttons .reset').on('click', () => {
            removeLocalStorageItem(LOCALSTORAGE_KEY);
            $(".listing-item.compact").animate({ marginLeft: '120%' }, 200, function(){
                $(".listing-item.compact").remove();
            });
            
            $('.compare-slide-menu .csm-message').removeClass('active');
        });

        // Send properties' slugs to compare page
        $('.btn-prop-compare').on('click', (e) => {
            e.preventDefault();
            const qString = setQueryString();
            const domain = e.target.href;
            const fullPath = domain.concat(qString);

            e.target.setAttribute("href", fullPath);
            window.location.href = e.target.href;
        });

        // Document events
        $window.on('load', ()  => {
            populateCompareContainer();
        });
    });
})(this.jQuery);