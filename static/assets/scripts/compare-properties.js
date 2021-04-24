(function ($) {
	'use strict';

	$(document).ready(() => {
		const $window = $(window);
		const compareSlideMenu = $('.compare-slide-menu');
		const compareProperties = $('.csm-properties');
		const SESSIONSTORAGE_KEY = 'compareProperties';
		const UNIQUE_STORAGE_OBJECT_NAME = 'propCollection';

		let retrieveSessionStorageItem = (lsKey) => {
			let lsCollection = null;

			if (sessionStorage.length !== 0 && !!sessionStorage[lsKey]) {
				lsCollection = JSON.parse(sessionStorage.getItem(lsKey));
				return lsCollection;
			} else {
				return false;
			}
		};

		let addSessionStorageItem = (lsKey, lsItem) => {
			removeSessionStorageItem(lsKey);
			sessionStorage.setItem(lsKey, JSON.stringify(lsItem));
		};

		let removeSessionStorageItem = (lsKey) => {
			if (sessionStorage.length !== 0 && !!sessionStorage[lsKey]) {
				sessionStorage.removeItem(lsKey);
			}
		};

		let collectAndStoreProperties = (props) => {
			const {
				currentStorage,
				sessionStorageKey,
				storageObjectName,
				propSlug,
				propHref,
				propPrice,
				propCoverImage,
				propTitle,
				propListingType,
			} = props;

			let propCollection = {};

			const propertyExists = currentStorage[storageObjectName].findIndex(
				(item) => item.propSlug === propSlug
			);

			if (propertyExists < 0) {
				propCollection = {
					propSlug: propSlug,
					propHref: propHref,
					propPrice: propPrice,
					propCoverImage: propCoverImage,
					propTitle: propTitle,
					propListingType: propListingType,
				};
				currentStorage[storageObjectName].push(propCollection);
				addSessionStorageItem(sessionStorageKey, currentStorage);
				populateCompareContainer(propCollection);
				return true;
			} else {
				return false;
			}
		};

		let populateCompareContainer = (propItem = null) => {
			const propText = {
				propCollection: [propItem],
			};
			const { propCollection } = propItem
				? propText
				: retrieveSessionStorageItem(SESSIONSTORAGE_KEY);
			const mappedProperties =
				!!propCollection &&
				propCollection.map((item) => {
					return (
						`<div class="listing-item compact inactive">` +
						`<a href="${item.propHref}" class="listing-img-container">` +
						`<div class="remove-from-compare" data-prop-slug="${item.propSlug}"></div>` +
						`<div class="listing-badges">` +
						`<span>${item.propListingType}</span>` +
						`</div>` +
						`<div class="listing-img-content">` +
						`<span class="listing-compact-title">${item.propTitle}<i>${item.propPrice}</i></span>` +
						`</div>` +
						`<img src="${item.propCoverImage}" alt="${item.propTitle}">` +
						`</a>` +
						`</div>`
					);
				});

			compareProperties.append(mappedProperties);

			propItem &&
				compareProperties
					.children('.listing-item:last-child')
					.animate({ marginLeft: '0' }, 200);
		};

		let removeProperty = (lsSlug) => {
			const oldPropCollection = retrieveSessionStorageItem(SESSIONSTORAGE_KEY);
			const currentStorage = { propCollection: [] };

			currentStorage.propCollection = oldPropCollection.propCollection.filter(
				(item) => item.propSlug !== lsSlug
			);
			addSessionStorageItem(SESSIONSTORAGE_KEY, currentStorage);
		};

		let setQueryString = () => {
			let qString = '';
			const { propCollection } = retrieveSessionStorageItem(SESSIONSTORAGE_KEY);
			propCollection.map((item) => {
				return (qString += `c=${item.propSlug}&`);
			});

			return qString;
		};

		/*----------------------------------------------------*/
		/*  Compare Menu
        /*----------------------------------------------------*/
		$('.csm-trigger').on('click', () => {
			compareSlideMenu.toggleClass('active');
			compareProperties
				.children('.listing-item.compact')
				.removeClass('inactive');
		});

		$('.csm-mobile-trigger').on('click', () => {
			compareSlideMenu.removeClass('active');
		});

		// Trigger set compare button
		$('.compare-button, .compare-widget-button').on('click', function () {
			const $this = $(this);
			const prevLsProperties = retrieveSessionStorageItem(SESSIONSTORAGE_KEY); // Retrieve previous properties
			const storageProps = {
				// Prepare data to set new storage
				currentStorage: { propCollection: [] },
				sessionStorageKey: SESSIONSTORAGE_KEY,
				storageObjectName: UNIQUE_STORAGE_OBJECT_NAME,
			};

			compareProperties
				.children('.listing-item.compact')
				.removeClass('inactive');

			!!prevLsProperties && (storageProps.currentStorage = prevLsProperties); // Update sessionStorage clone

			// Store new property to compare
			if (storageProps.currentStorage.propCollection.length <= 2) {
				$.ajax({
					type: 'POST',
					url: `/listings/get_json_data/`,
					async: true,
					dataType: 'json',
					data: { propSlug: $this.data('slug') },
					success: function (res) {
						const { propData } = res;
						const storagePropsWithData = { ...storageProps, ...propData };

						if (collectAndStoreProperties(storagePropsWithData) === false) {
							const toastOptions = {
								toastType: 'warning',
								toastMsg: 'Property is already being comapred!',
							};

							addToast(toastOptions); // toast function from global script (currently najdistan-script.js)
						}
					},
					error: function (xhr, status, err) {
						console.log(xhr, err);
					},
					// complete: function(){
					//     console.log('data pull complete');
					// }
				});
			} else {
				const toastOptions = {
					toastType: 'error',
					toastMsg: 'Max capacity reached for compare properties!',
				};

				addToast(toastOptions); // toast function from global script (currently najdistan-script.js)
			}

			!compareSlideMenu.hasClass('active') &&
				compareSlideMenu.addClass('active');
		});

		// Remove property from compare list
		compareProperties.on('click', $('.remove-from-compare'), (e) => {
			let propSlug = e.target.getAttribute('data-prop-slug');

			if (propSlug) {
				e.preventDefault();
				removeProperty(propSlug);

				$(e.target.parentNode.parentNode).animate(
					{ marginLeft: '120%' },
					200,
					function () {
						$(e.target.parentNode.parentNode).remove();
					}
				);
			}
		});

		// Reset local storage
		$('.csm-buttons .reset').on('click', () => {
			removeSessionStorageItem(SESSIONSTORAGE_KEY);
			$('.listing-item.compact').animate(
				{ marginLeft: '120%' },
				200,
				function () {
					$('.listing-item.compact').remove();
				}
			);
		});

		// Send properties' slugs to compare page
		$('.btn-prop-compare').on('click', (e) => {
			e.preventDefault();
			const { propCollection } = retrieveSessionStorageItem(SESSIONSTORAGE_KEY);

			if (!!propCollection && propCollection.length < 2) {
				const toastOptions = {
					toastType: 'warning',
					toastMsg: 'At least two properties are required to compare!',
				};

				addToast(toastOptions);
			} else {
				const qString = setQueryString();
				const domain = e.target.href;
				const fullPath = domain.concat(qString);

				e.target.setAttribute('href', fullPath);
				window.location.href = e.target.href;
			}
		});

		// Document events
		//$window.on('load', ()  => {
		populateCompareContainer();
		//});
	});
})(this.jQuery);
