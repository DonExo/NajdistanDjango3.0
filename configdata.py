PROJECT_NAME = "Najdistan v3.0"

LOGIN_COOKIE_EXPIRY = 1209600  # in seconds, equals to 2 weeks

LISTING_TYPE = (
    ('rent', 'For rent'),
    ('sell', 'For sell')
)

HOME_TYPE = (
    ('apartment', 'Apartment'),
    ('house', 'House')
)

INTERIOR_CHOICES = (
    ('unfurnished', 'Non furnished'),
    ('upholstered', 'Semi furnished'),
    ('furnished', 'Fully furnished'),
    ('unspecified', 'Not specified')
)

HEATING_CHOICES = (
    ('central', 'Central heating'),
    ('solar', 'Solar energy'),
    ('electricity', 'Electricity'),
    ('gas', 'Gas'),
    ('wood', 'Wood stove'),
    ('other', 'Other...'),
    ('none', 'None')
)

UPDATE_FREQUENCIES = (
    ('daily', "Daily"),
    ('weekly', "Weekly"),
    ('biweekly', "Bi-weekly"),
    ('monthly', "Monthly"),
    ('instant', "Instantly") # Paid version !
)

# @TODO: To be filled with all relevant data or, some data migration for this? Yet to be decided on the business logic of adding cities
REGIONS_AND_CITIES = {
    'Drenthe' : ['Assen', 'Coevorden', 'Emmen', 'Hoogeveen', 'Meppel'],
    'Flevoland': ['Almere', 'Biddinghuizen', 'Emmeloord', 'Lelystad'],
    'Friesland': ['Bolsward', 'Dokkum', 'Franeker', 'Harlingen', 'Hindeloopen', 'IJlst','Leeuwarden', 'Sloten', 'Sneek', 'Stavoren', 'Workum']
}

REGEX_ZIPCODE_VALIDATOR = ".*?"  # Change this to apply restrictions to zip-code
REGEX_TELEPHONE_VALIDATOR = '^\+*[0-9]*$'  # Change this to apply phone number restrictions, i.e: '^(\+\d{1,3})?,?\s?\d{8,13}'
FORBIDDEN_MESAGE = "You don't have sufficient access to do this action"
PAGINATOR_ITEMS_PER_PAGE = 5
