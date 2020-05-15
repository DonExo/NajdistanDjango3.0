PROJECT_NAME = "Najdistan v3.0"

LOGIN_COOKIE_EXPIRY = 1209600  # in seconds, equals to 2 weeks

LISTING_TYPE = (
    ('rent', 'For rent'),
    ('sell', 'For sell')
)

LISTING_TYPE_2 = (
    ('rent', 'For rent'),
    ('buy', 'For buy')
)

HOME_TYPE = (
    ('house', 'A house'),
    ('apartment', 'An apartment')
)

INTERIOR_CHOICES = (
    ('unspecified', 'Not specified'),
    ('furnished', 'Fully furnished'),
    ('unfurnished', 'Non furnished'),
    ('upholstered', 'Semi furnished')
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

# @TODO: To be filled with all relevant data
REGIONS_AND_CITIES = {
    'Drenthe' : ['Assen', 'Coevorden', 'Emmen', 'Hoogeveen', 'Meppel'],
    'Flevoland': ['Almere', 'Biddinghuizen', 'Emmeloord', 'Lelystad'],
    'Friesland': ['Bolsward', 'Dokkum', 'Franeker', 'Harlingen', 'Hindeloopen', 'IJlst','Leeuwarden', 'Sloten', 'Sneek', 'Stavoren', 'Workum']
}

REGEX_ZIPCODE_VALIDATOR = "^[0-9]{4}[a-zA-Z]{2}$"

FORBIDDEN_MESAGE = "You don't have sufficient access to do this action"

PAGINATOR_ITEMS_PER_PAGE = 5
